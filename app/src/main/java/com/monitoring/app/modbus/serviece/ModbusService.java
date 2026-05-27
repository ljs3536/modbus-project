package com.monitoring.app.modbus.serviece;

import com.intelligt.modbus.jlibmodbus.ModbusMaster;
import com.intelligt.modbus.jlibmodbus.ModbusMasterFactory;
import com.intelligt.modbus.jlibmodbus.tcp.TcpParameters;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import java.net.InetAddress;
import java.nio.ByteBuffer;

@Service
public class ModbusService {

    private float latestSensorValue = 0.0f;
    private ModbusMaster master;

    public ModbusService() {
        try {
            // docker-compose.yml에 정의된 게이트웨이 이름으로 접속
            TcpParameters tcpParameters = new TcpParameters();
            tcpParameters.setHost(InetAddress.getByName("modbus-gateway"));
            tcpParameters.setPort(502);
            tcpParameters.setKeepAlive(true);

            master = ModbusMasterFactory.createModbusMasterTCP(tcpParameters);
            master.connect();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 1초마다 게이트웨이에서 데이터 읽어오기
    @Scheduled(fixedRate = 1000)
    public void pollModbusData() {
        try {
            if (!master.isConnected()) master.connect();

            // 40001번 주소(offset 0)부터 2개의 방(레지스터)을 읽어옴
            int[] registers = master.readHoldingRegisters(1, 0, 2);

            // 💡 16비트 정수 2개를 32비트 Float로 디코딩 (Python struct.pack과 반대 과정)
            ByteBuffer buffer = ByteBuffer.allocate(4);
            buffer.putShort((short) registers[0]);
            buffer.putShort((short) registers[1]);
            buffer.flip(); // 버퍼 읽기 모드로 전환

            latestSensorValue = buffer.getFloat();
            System.out.println("수신 및 디코딩 완료: " + latestSensorValue);

        } catch (Exception e) {
            System.out.println("데이터 읽기 실패: " + e.getMessage());
        }
    }

    public float getLatestSensorValue() {
        return latestSensorValue;
    }
}