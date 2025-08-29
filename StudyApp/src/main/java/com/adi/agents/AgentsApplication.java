package com.adi.agents;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.kafka.annotation.EnableKafka;

@EnableKafka
@SpringBootApplication
public class AgentsApplication {

	public static void main(String[] args) {
		SpringApplication.run(AgentsApplication.class, args);
	}

}
