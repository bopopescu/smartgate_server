# smartgate_server

IoT 기반 스마트게이트 동작을 위한 서버입니다.

virtenv 폴더에는 버전관리를 하기 위하여 가상환경을 적용하였으며 해당 환경에 설치되어 있는 라이브러리는 다음과 같습니다.  
django 3.0.5  
pymysql 0.9.3  
django suit 0.2.28  

smartgate 폴더에는 django 를 활용한 서버구현과 관련된 코드가 작성되어 있고 각 폴더(앱) 마다 지원하는 기능은 다음과 같습니다.  
hotelreserv - 애플리케이션과 아두이노의 연동을 위한 소스코드가 작성되어 있습니다.    
              주 기능은 views.py 에 작성되어 있으며 회원정보 조회, 해당 날짜에 예약된 방 정보 출력, 사용자가 선택한 방 예약,  
              예약 취소 등의 기능이 구현되어 있습니다.  
Identification - 데이터베이스에 존재하는 데이터를 불러와서 웹 화면을 구성하는 코드가 작성되어 있습니다.  
                 주 기능은 admin.py 와 models.py 에 작성되어 있으며 각 .py가 구현하는 내용은 다음과 같습니다.  
                 
admin.py - 데이터베이스에 존재하는 데이터들을 models.py 에게 받아와서 출력하고 정렬할 수 있는 기능을 구현합니다.    
            추가적으로 여러 데이터들을 한꺼번에 수정하거나 필터를 적용할 수 있습니다.  
              
models.py - 데이터베이스에서 받은 테이블을 객체화하고 그 객체에 데이터베이스에 존재하는 데이터를 받아와 개발자가 데이터베이스 접근을 
            용이하게 해주는 기능입니다.  
              
