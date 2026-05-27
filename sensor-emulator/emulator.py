import time
import struct
import logging
from pymodbus.client import ModbusTcpClient

# 로그 설정 (터미널에서 전송 상태를 보기 위함)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# 진석 님의 실제 센서 데이터 샘플
SENSOR_DATA = [
    0.022780273109674454, 0.02690768428146839, 0.019691605120897293, 
    0.015416556037962437, 0.013577992096543312, 0.01773606240749359, 
    0.019724803045392036, 0.022973010316491127, 0.017965108156204224
]

def float_to_modbus_registers(float_val):
    """
    32비트 실수(Float)를 Modbus용 16비트 정수(Register) 2개로 변환 (Encoding)
    """
    # 1. Float를 4바이트(32비트) 메모리 구조로 패킹 (>f: Big-Endian 방식의 float)
    packed_bytes = struct.pack('>f', float_val)
    
    # 2. 패킹된 4바이트를 2바이트(16비트) 정수 2개로 언패킹 (>HH: Big-Endian 방식의 Unsigned Short 2개)
    reg1, reg2 = struct.unpack('>HH', packed_bytes)
    
    return [reg1, reg2]

def run_emulator():
    client = ModbusTcpClient('modbus-gateway', port=502)
    
    # --- 수정된 부분: 연결될 때까지 무한 재시도 ---
    connected = False
    while not connected:
        logging.info("⏳ 게이트웨이 연결 시도 중...")
        connected = client.connect()
        
        if connected:
            logging.info("✅ Modbus 게이트웨이에 연결 성공!")
        else:
            logging.warning("게이트웨이가 아직 준비되지 않았습니다. 3초 후 다시 시도합니다...")
            time.sleep(3)
    # ---------------------------------------------
            
    # 연결 성공 후 데이터 전송 루프
    index = 0
    while True:
        current_value = SENSOR_DATA[index % len(SENSOR_DATA)]
        registers = float_to_modbus_registers(current_value)
        
        try:
            client.write_registers(address=0, values=registers, slave=1)
            logging.info(f"전송 완료 | 원본: {current_value:.6f} -> Modbus: {registers}")
        except Exception as e:
            logging.error(f"전송 중 에러 발생: {e}")
            
        index += 1
        time.sleep(1)
        
if __name__ == "__main__":
    run_emulator()