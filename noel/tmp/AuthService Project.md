
application.yml
``` bash
spring:  
  datasource:  
    url: jdbc:mariadb://localhost:3307/auth  
    username: root  
    password: adminadmin  
    driver-class-name: org.mariadb.jdbc.Driver  
  
  jpa:  
    hibernate:  
      ddl-auto: update  
    show-sql: true  
    database-platform: org.hibernate.dialect.MariaDBDialect  
  
server:  
  port: 8081
```
pom.xml
``` bash
<dependencyManagement>  
    <dependencies>
	    <dependency>
		    <groupId>org.springframework.boot</groupId>  
            <artifactId>spring-boot-dependencies</artifactId>  
            <version>${spring.boot.version}</version>  
            <type>pom</type>  
            <scope>import</scope>  
        </dependency>
    </dependencies>
</dependencyManagement>
<dependencies>  
    <dependency>
	    <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-web</artifactId>  
    </dependency>  
    <dependency>
	    <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-data-jpa</artifactId>  
    </dependency>
    <dependency>
	    <groupId>org.mariadb.jdbc</groupId>  
        <artifactId>mariadb-java-client</artifactId>  
    </dependency>  
    <dependency>
	    <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-security</artifactId>  
    </dependency>  
    <dependency>
	    <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-validation</artifactId>  
    </dependency>  
    <dependency>
	    <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-test</artifactId>  
        <scope>test</scope>  
    </dependency></dependencies>
<build>  
    <plugins>
	    <plugin>
		    <groupId>org.springframework.boot</groupId>  
            <artifactId>spring-boot-maven-plugin</artifactId>  
        </plugin>
    </plugins>
</build>
```

Project structure:
