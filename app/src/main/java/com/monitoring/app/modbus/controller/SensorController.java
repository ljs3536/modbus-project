package com.monitoring.app.modbus.controller;

import com.monitoring.app.modbus.serviece.ModbusService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

@RestController
public class SensorController {

    private final ModbusService modbusService;

    public SensorController(ModbusService modbusService) {
        this.modbusService = modbusService;
    }

    // 화면 띄우기
    @GetMapping("/")
    public ModelAndView index() {
        return new ModelAndView("index");
    }

    // 차트에서 1초마다 호출할 실시간 데이터 API
    @GetMapping("/api/data")
    public float getSensorData() {
        return modbusService.getLatestSensorValue();
    }
}
