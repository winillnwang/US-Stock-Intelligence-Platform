# US Stock Intelligence Platform



美股資料分析與投資資訊平台



## Project Overview



US Stock Intelligence Platform 是一個以 Python、Django、MySQL 建立的美股資料分析與後端資料服務專案。

系統整合外部股票 API，將每日 OHLCV 股價資料經過資料清理、驗證與轉換後寫入 MySQL，並透過 Django ORM、Pandas 與 Django REST Framework 提供股票查詢、歷史價格、資料分析與 REST API。

本專案著重於後端工程與資料流程設計，包含 JWT Authentication、Data Pipeline、Data Quality Validation、Logging、Exception Handling、Automated Tests、Docker、GitHub Actions CI 與 OpenAPI / Swagger 文件。


## System Architecture

The platform follows an end-to-end data pipeline—from external market data ingestion and quality validation to analytics and secure API delivery.

![US Stock Intelligence Platform architecture](docs/images/us-stock-intelligence-platform-architecture.png)

> Alpha Vantage API → Data Ingestion → Validation → MySQL → Pandas Analysis → Django REST API → JWT Authentication → Swagger / Client

<details>
<summary><strong>View Mermaid architecture diagram</strong></summary>

```mermaid
flowchart LR
    subgraph S1["1 · Data Acquisition"]
        direction TB
        A["Alpha Vantage API"] --> B["Requests"]
        B --> C["Fetch Daily Prices"]
    end

    subgraph S2["2 · Processing & Quality"]
        direction TB
        D["Transform / Clean"] --> E["Data Quality Validation"]
    end

    subgraph S3["3 · Storage & Analytics"]
        direction TB
        F["Django ORM"] --> G[("MySQL")]
        G --> H["Pandas Analysis"]
    end

    subgraph S4["4 · Application & Delivery"]
        direction TB
        I["Django Web / REST API"] --> J["JWT Authentication"]
        J --> K["Swagger / Client"]
    end

    C --> D
    E --> F
    H --> I

    subgraph SUPPORT["Cross-cutting Engineering & Operations"]
        direction TB
        L["Logging"]
        M["Exception Handling"]
        N["Automated Tests"]
        O["Docker"]
        P["GitHub Actions CI"]
    end

    L -.-> C
    L -.-> I
    M -.-> E
    M -.-> I
    N -.-> E
    N -.-> I
    O -.-> G
    O -.-> I
    P -.-> N
    P -.-> O

    classDef source fill:#E0F2FE,stroke:#0284C7,color:#0C4A6E,stroke-width:2px;
    classDef process fill:#EDE9FE,stroke:#7C3AED,color:#4C1D95,stroke-width:2px;
    classDef data fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
    classDef delivery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
    classDef support fill:#F1F5F9,stroke:#64748B,color:#0F172A,stroke-width:1.5px;

    class A,B,C source;
    class D,E process;
    class F,G,H data;
    class I,J,K delivery;
    class L,M,N,O,P support;

    style S1 fill:#F8FCFF,stroke:#38BDF8,stroke-width:2px
    style S2 fill:#FBF9FF,stroke:#A78BFA,stroke-width:2px
    style S3 fill:#F7FFF9,stroke:#4ADE80,stroke-width:2px
    style S4 fill:#FFFCF5,stroke:#FBBF24,stroke-width:2px
    style SUPPORT fill:#F8FAFC,stroke:#94A3B8,stroke-width:2px,stroke-dasharray:6 4
```

</details>

## Tech Stack



- Python 3.14
- Django 6.1
- Django REST Framework
- Simple JWT
- drf-spectacular
- MySQL 8.4
- Django ORM
- Pandas
- NumPy
- Requests
- HTML / CSS / JavaScript
- Docker
- Docker Compose
- GitHub Actions
- Git / GitHub



## Project Status



🚧 Under Development

目前核心後端功能已完成，包含 REST API、JWT Authentication、Data Pipeline、Data Quality Validation、Logging、Exception Handling、Automated Tests、Docker、GitHub Actions CI 與 OpenAPI / Swagger 文件。

目前進入專案文件整理、架構圖、Demo 與面試準備階段。



## Features

- 股票搜尋與個股詳細資訊
- 歷史 OHLCV 股價資料查詢
- Pandas 技術分析
  - 5 / 10 / 20 日平均收盤價
  - 報酬率
  - 波動率
  - 成交量變化
  - 30 日高低點距離
- REST API
- JWT Authentication
- Alpha Vantage Data Pipeline
- Data Quality Validation
- Logging 與 Exception Handling
- Automated Tests
- Docker / Docker Compose
- GitHub Actions CI
- OpenAPI / Swagger API Documentation
