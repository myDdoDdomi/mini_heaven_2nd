# 웹소켓 통신을 이용한 실시간 게임

# 목차

1. [기획 배경](#기획-배경)
2. [팀원 소개](#팀원-소개)
3. [서비스 소개](#서비스-소개)
4. [기술 스택](#기술-스택)
5. [주요 알고리즘](#주요-알고리즘)

# 기획 배경

## 목적

- 알고리즘 학습 기간에 더 효율적인 학습 방법을 찾고자 실무적으로 활용 가능한 프로젝트를 진행.
- 특히 Python의 문법 구조, 객체 지향 프로그래밍(class) 등을 실제 프로젝트에서 접목하여 이해를 높임.


# 팀원 소개
![](image/게임팀원.png)

# 서비스 소개

- 이 프로젝트는 SSAFY 내 반 친구들을 대상으로 진행한 'SSAFY데이' 이벤트를 위해 개발된 실시간 PvP 게임 서비스입니다. 총 3가지 게임 모드로 구성되어 있으며, 각각의 게임을 통해 이벤트 승자를 가리는 것을 목표로 했습니다.

- 제공게임
  - 네코팡(애니팡): 같은 모양의 블록을 터뜨리는 퍼즐 게임
  - 퐁당(알까기): 상대의 공을 밀어내는 전략 게임
  - 러브밤(포트리스): 포탄을 쏘아 상대를 공격하는 슈팅 게임
  - 폴더 안 리드미 확인 가능
    
## 기술 스택

### Pygame

- Pygame을 활용하면 게임 개발을 통해 프로그래밍의 기본 개념과 알고리즘을 시각적으로 이해
- 이를 이용한 실시간 상호작용 및 이벤트 처리

### WebSocket

- 클라이언트와 서버 간의 실시간 양방향 통신 가능, 실제 네트워크 환경에서의 데이터 전송과 비동기 처리를 경험
- 실시간 통신의 효율성과 네트워크 프로그래밍에 대한 이해도를 높임

### 주요 알고리즘

#### 1. 네코팡
- 매칭 알고리즘
  - 같은 종류의 블록을 확인하고 3개 이상 연속된 블록을 찾아내어 제거 대상으로 지정합니다. 블록의 좌우, 상하를 모두 검사하여 일치하는 블록을 찾아내는 것이 핵심
- 블록 드롭 알고리즘
  - 매칭된 블록이 제거된 후 위에 있는 블록들이 아래로 자연스럽게 떨어지도록 합니다. 이때 상단의 빈 공간은 새로운 블록으로 채워 게임의 흐름을 지속
   
#### 2. 퐁당 (Pongdang)
- 오브젝트 충돌 및 물리 엔진
  - 공이 벽이나 다른 오브젝트와 충돌할 때 각도와 속도 변화가 실제 물리 법칙에 따라 움직이도록 하는 알고리즘
- 캡 배치 알고리즘
  - 게임 시작 시 플레이어의 캡 위치를 랜덤으로 배치하되, 겹치지 않도록 위치를 조정하는 알고리즘
 
#### 3. 러브밤 (Love Bomb)
- 발사체 궤적 계산 알고리즘
  - 발사체의 궤적을 계산하여 바람의 방향, 속도, 각도에 따라 움직임을 결정하는 알고리즘
- 환경 변화 알고리즘
  - 게임 내 계절 변화를 시뮬레이션하며, 각 계절별 풍속, 저항값 등을 조정하여 게임 난이도를 변화
 
#### 4. 웹소켓
- 실시간 데이터 전송 및 동기화
  - 서버와 클라이언트 간의 양방향 통신을 통해 게임 상태, 플레이어의 움직임 등을 실시간으로 동기화하는 알고리즘
- 상태 업데이트 및 관리
  - 각 클라이언트의 상태를 서버에서 주기적으로 업데이트하고 이를 클라이언트들에게 전달하는 동기화 알고리즘

