# QuantConsole — Orchestration & Lifecycle Graph

Visual reference for service orchestration, event dispatch, and the signal-to-fill pipeline.

---

## 1. Bootstrap Sequence

```mermaid
flowchart TD
    A([main.py]) --> B[DeltaExchangeClient
    create REST client]
    B --> C[fetch_history
    750 historical candles]
    C --> D[IndicatorService
    compute_indicators
    KFMA · EWMA vol · URSI]
    D --> E[FeatureEngine
    compute_features
    6-feature matrix + fit RobustScaler]
    E --> F[RegimeDetector
    fit GaussianHMM
    BIC model selection]
    F --> G[ChartManager
    setup_chart
    candlestick + regime session bands]
    G --> H[HawkesService
    setup_chart
    intensity chart + internal WS callbacks]
    H --> I[DeltaStreamManager
    register services
    see Registration Order]
    I --> J[asyncio.create_task
    manager.connect
    WebSocket → stream forever]
    J --> K([Live streaming loop])
```

---

## 2. Service Registration Order

Services are registered sequentially; order governs the `on_bar` execution sequence.

```mermaid
flowchart LR
    M[DeltaStreamManager] -->|1 on_bar| RD[RegimeDetector]
    M -->|2 on_bar + on_tick| IS[IndicatorService]
    M -->|3 on_bar + on_tick
    + on_trade + on_l2_updates| SS[StrategyService]
    M -->|4 on_bar + on_tick| RS[RiskService]
    M -->|5 on_tick only| PS[PositionService]
```

---

## 3. Event Dispatch Model

```mermaid
flowchart TD
    WS([Delta Exchange WebSocket]) --> DSM[DeltaStreamManager]

    DSM -->|bar event
    ⚡ sequential await| BAR_CHAIN

    subgraph BAR_CHAIN["on_bar — awaited in order"]
        direction TB
        B1[1 · RegimeDetector
        predict regime · current_regime
        maybe_refit every N bars]
        B2[2 · IndicatorService
        append confirmed bar · drop oldest
        state.df sync]
        B3[3 · StrategyService
        read current_regime
        dispatch to active strategy]
        B4[4 · RiskService
        stop check · drawdown check]
        B1 --> B2 --> B3 --> B4
    end

    DSM -->|candlestick event
    🔀 fire-and-forget tasks| CANDLE_TASKS

    subgraph CANDLE_TASKS["on_tick — concurrent tasks"]
        direction LR
        C1[IndicatorService
        patch live OHLCV
        update indicators · push chart]
        C2[StrategyService
        BullishStrategy.on_tick]
        C3[RiskService
        intrabar stop check
        vs candle.low/high]
        C4[PositionService
        MTM · MAE update]
    end

    DSM -->|all_trades event
    🔀 fire-and-forget| TRADE_TASKS

    subgraph TRADE_TASKS["on_trade — concurrent tasks"]
        T1[StrategyService
        CrisisStrategy.on_trade]
        T2[HawkesService
        classify BUY·SELL·WHALE
        update λ accumulators]
    end

    DSM -->|l2_updates event
    🔀 fire-and-forget| L2_TASKS

    subgraph L2_TASKS["on_l2_updates — concurrent tasks"]
        L1[StrategyService
        ConsolidationStrategy.on_l2_updates]
    end
```

---

## 4. Signal Pipeline — Entry

```mermaid
flowchart TD
    SS[StrategyService
    on_bar · on_tick · on_trade · on_l2_updates]
    SS --> STRAT["Active BaseStrategy
    (regime-matched)"]
    STRAT -->|Signal or None| CHK{Signal
    generated?}
    CHK -->|None| DROP1([drop — no action])
    CHK -->|Signal| EV[EVService.evaluate]

    EV --> GATE{EV > 0
    and not is_exit?}
    GATE -->|EV ≤ 0| DROP2([reject signal
    EV gate])
    GATE -->|EV > 0 or is_exit| ANNOTATE[annotate ev_score
    kelly_fraction half-Kelly ≤ 20%]
    ANNOTATE --> RISK[RiskService.evaluate]

    RISK --> RGATE{Passes risk
    checks?}
    RGATE -->|fail| DROP3([reject signal
    risk gate])
    RGATE -->|pass| EXEC[ExecutionService.execute]

    EXEC --> MODE{PAPER_TRADING?}
    MODE -->|True| PAPER[_paper_execute
    simulated fill]
    MODE -->|False| LIVE[_live_execute
    Delta REST POST /v2/orders]

    PAPER --> FILL[PositionService.on_fill]
    LIVE --> FILL

    FILL --> POSTYPE{Entry or Exit?}
    POSTYPE -->|Entry| OPEN[open Position
    TradeLogService.log_entry]
    POSTYPE -->|Exit| CLOSE[close Position
    compute realized PnL
    TradeLogService.log_exit
    EVService.record_outcome]
```

---

## 5. Signal Pipeline — Force Exit (Risk-Manager)

```mermaid
flowchart TD
    RB[RiskService.on_bar
    or on_tick] --> DETECT{Stop hit
    or drawdown
    breach?}
    DETECT -->|No| IDLE([continue])
    DETECT -->|Yes| FE[_force_exit
    build FLAT Signal
    is_exit=True]
    FE --> EXEC[ExecutionService.execute]
    EXEC --> FILL[PositionService.on_fill
    close Position]
    FILL --> LOG[TradeLogService.log_exit
    EVService.record_outcome]
```

---

## 6. Strategy-Initiated Exit

```mermaid
flowchart TD
    SS[StrategyService.on_bar
    or on_tick] --> ESTRAT["BaseStrategy.exit_signal
    (state, position, regime)"]
    ESTRAT -->|Signal is_exit=True| EV[EVService.evaluate
    skip EV gate
    forward unconditionally]
    EV --> RISK[RiskService.evaluate]
    RISK --> EXEC[ExecutionService.execute]
    EXEC --> FILL[PositionService.on_fill]
    FILL --> LOG[TradeLogService.log_exit
    EVService.record_outcome]
```

---

## 7. HawkesService — Parallel Intensity Pipeline

HawkesService is **not yet a StreamService**. It owns its own internal WS callbacks.

```mermaid
flowchart TD
    WS([Delta Exchange WebSocket])

    subgraph HAWK["HawkesService (isolated pipeline)"]
        direction TB
        H1[on_trade callback
        classify event dimension
        BUY · SELL · WHALE]
        H2[update λ accumulators _R
        O1 recursive decay
        half-life 60 s]
        H3[on_bar callback
        check VOL_SURGE · PRICE_SHOCK
        live intensity λ_j = μ_j + α · R_j]
        H4{Every hawkes_refit_bars?}
        H5[L-BFGS-B MLE refit
        wall-time ≤ hawkes_refit_max_ms
        update μ · α]
        H6[chart.update
        5 intensity lines
        info table λ · μ · λ/μ · spike alert]
        H1 --> H2 --> H3 --> H4
        H4 -->|Yes| H5 --> H6
        H4 -->|No| H6
    end

    WS -->|all_trades| H1
    WS -->|bar| H3
```

---

## 8. Full Service Dependency Graph

```mermaid
flowchart TD
    CFG[config.py
    SYMBOL · TIMEFRAME · TIMEFRAME_CONFIG]
    MDL[models.py
    StreamState · Signal · Order · Position]

    EXC[DeltaExchangeClient
    exchange_service.py]
    DSM[DeltaStreamManager
    streaming_service.py]
    IND[IndicatorService
    indicator_service.py]
    FEA[FeatureEngine
    feature_service.py]
    REG[RegimeDetector
    regime_service.py]
    CHT[ChartManager
    chart_service.py]
    HAW[HawkesService
    hawkes_service.py]
    STR[StrategyService
    strategy_service.py]
    EV[EVService
    ev_service.py]
    RSK[RiskService
    risk_service.py]
    EXS[ExecutionService
    execution_service.py]
    POS[PositionService
    position_service.py]
    TLS[TradeLogService
    trade_log_service.py]

    CFG --> DSM
    CFG --> EXC
    EXC --> DSM
    EXC --> HAW

    DSM --> IND
    DSM --> REG
    DSM --> STR
    DSM --> RSK
    DSM --> POS

    IND --> FEA
    FEA --> REG
    REG --> STR
    IND --> CHT
    REG --> CHT
    HAW --> CHT

    STR --> EV
    EV --> RSK
    RSK --> EXS
    EXS --> POS
    EXS --> TLS
    POS --> TLS
    POS --> EV

    MDL -.->|StreamState| DSM
    MDL -.->|Signal| STR
    MDL -.->|Order| EXS
    MDL -.->|Position| POS
```
