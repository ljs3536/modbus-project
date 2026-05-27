import logging
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# 터미널에 로그를 예쁘게 찍기 위한 설정
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def run_server():
    # Holding Register (40001번~) 주소에 0으로 채워진 빈 방 100개(메모리) 생성
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 100) 
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    logging.info("✅ 나만의 Modbus 게이트웨이 서버가 502번 포트에서 가동을 시작했습니다!")
    
    # 0.0.0.0:502 로 서버 실행 (모든 컨테이너의 접속 허용)
    StartTcpServer(context=context, address=("0.0.0.0", 502))

if __name__ == "__main__":
    run_server()