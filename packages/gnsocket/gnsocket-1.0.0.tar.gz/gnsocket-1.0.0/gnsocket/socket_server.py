# Standar lib
import asyncio
import functools
from multiprocessing import Manager, Queue, Lock

# contrib modules
import ujson as json

# Own module
from gnsocket.gn_socket import GNCSocket
from gnsocket.socket_base import GNCSocketBase

# module tasktools
from tasktools.taskloop import coromask, renew, simple_fargs_out
from networktools.colorprint import gprint, bprint, rprint

from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps

from basic_queuetools.queue import read_queue_gen, send_queue

tsleep = 2


class GNCSocketServer(GNCSocketBase):

    def __init__(self, queue_n2t, queue_t2n, *args, **kwargs):
        super().__init__(queue_n2t, queue_t2n, 'server', *args, **kwargs)
        self.set_socket_task(self.socket_task)

    def socket_task(self):
        with GNCSocket(mode=self.mode, timeout=self.timeout, raise_timeout=self.raise_timeout, log_path=self.log_path) as gs:
            loop = asyncio.get_event_loop()
            self.loop = loop
            gs.set_address(self.address)
            gs.set_loop(loop)
            try:
                async def socket_io(reader, writer):
                    idc = await gs.set_reader_writer(reader, writer)
                    # First time welcome
                    welcome = json.dumps(
                        {"msg": "Welcome to socket", 'idc_server': idc})
                    await gs.send_msg(welcome, idc)
                    await asyncio.sleep(0.1)
                    # task reader
                    try:
                        args = [gs, idc]
                        task_1 = loop.create_task(
                            coromask(
                                self.sock_read,
                                args, {},
                                simple_fargs_out)
                        )
                        task_1.add_done_callback(
                            functools.partial(
                                renew,
                                task_1,
                                self.sock_read,
                                simple_fargs_out)
                        )
                        args = [gs, idc]
                        # task write
                        task_2 = loop.create_task(
                            coromask(
                                self.sock_write,
                                args, {},
                                simple_fargs_out)
                        )
                        task_2.add_done_callback(
                            functools.partial(
                                renew,
                                task_2,
                                self.sock_write,
                                simple_fargs_out)
                        )
                    except Exception as exe:
                        raise exe
                future = loop.create_task(
                    gs.create_server(socket_io, loop))
                if not loop.is_running():
                    loop.run_forever()
                else:
                    loop.run_until_complete(future)
            except KeyboardInterrupt as k:
                print("Closing with keyboard")
                gs.logger.exception("Cierre forzado desde teclado %s" %ex)                
                loop.run_until_complete(gs.wait_closed())
                raise k
            except Exception as ex:
                gs.logger.exception("Error con modulo cliente gnsocket %s" %ex)                                
                print("Otra exception", ex)
                raise ex
            finally:
                print("Clossing loop on server")
                loop.close()

        def close(self):
            self.gs.close()
