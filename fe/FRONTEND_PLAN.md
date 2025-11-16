# 좌석 예약 시스템 프론트엔드 기획서

## 1. 프로젝트 개요

연말 총회용 테이블 좌석 예약 시스템

### 핵심 기능
- 에피소드별 테이블 레이아웃 관리
- 원형 테이블 생성 및 위치 조절 (드래그 앤 드롭)
- 테이블별 좌석 수 설정
- (추후) 좌석 예약 기능

---

## 2. 화면 구성

```
┌─────────────────────────────────────────┐
│              헤더 (Header)                │
│  - 시스템 제목                           │
│  - 에피소드 선택/생성                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│          무대 / 모니터 영역               │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│            테이블 영역 (Floor)            │
│                                         │
│     ○ 테이블1    ○ 테이블2              │
│       (8석)        (10석)               │
│                                         │
│            ○ 테이블3                     │
│              (6석)                       │
│                                         │
│  * 테이블을 드래그하여 위치 조절           │
│  * 클릭하여 좌석 수 변경                  │
└─────────────────────────────────────────┘

┌──────────┐
│ 테이블    │ (선택 시 나타나는 사이드 패널)
│ 설정      │
│ - 좌석 수 │
│ - 삭제    │
└──────────┘
```

---

## 3. 컴포넌트 구조

```
src/
├── components/
│   ├── Header/
│   │   └── Header.tsx
│   ├── Stage/
│   │   └── Stage.tsx
│   ├── Floor/
│   │   ├── Floor.tsx
│   │   └── Table.tsx
│   ├── TableSettings/
│   │   └── TableSettings.tsx
│   └── EpisodeSelector/
│       └── EpisodeSelector.tsx
├── hooks/
│   └── useEpisodes.ts
├── types/
│   └── index.ts
├── styles/
│   └── (컴포넌트별 CSS 또는 styled-components)
├── App.tsx
└── main.tsx
```

---

## 4. 데이터 모델

```typescript
interface Table {
  id: string;
  name: string;
  x: number;        // 위치 X
  y: number;        // 위치 Y
  seats: number;    // 좌석 수
}

interface Episode {
  id: string;
  name: string;
  tables: Table[];
}
```

---

## 5. 구현 단계

### Phase 1: 기본 구조 (현재)
1. ✅ 프로젝트 초기 설정 (Vite + React + TypeScript)
2. ✅ 드래그 앤 드롭 라이브러리 설치 (react-draggable)
3. 🔄 컴포넌트 파일 분리
4. 🔄 기본 레이아웃 구현

### Phase 2: 핵심 기능
5. 테이블 생성/삭제
6. 테이블 드래그 이동
7. 좌석 수 조절
8. 에피소드 관리

### Phase 3: 예약 기능 (추후)
9. 좌석별 예약 UI
10. 예약자 정보 입력
11. 예약 상태 표시
12. 백엔드 API 연동

---

## 6. 기술 스택

- **Framework**: React 19 + TypeScript
- **Build Tool**: Vite 7
- **Drag & Drop**: react-draggable
- **상태관리**: React useState (추후 필요시 Zustand)
- **스타일링**: CSS Modules 또는 Styled Components

---

## 7. 다음 작업

1. **컴포넌트 분리**: App.tsx를 여러 컴포넌트로 분리
2. **커스텀 훅 생성**: 에피소드/테이블 상태 관리 로직 분리
3. **타입 정리**: types 폴더에 인터페이스 정리
4. **스타일 모듈화**: 컴포넌트별 CSS 파일 분리
