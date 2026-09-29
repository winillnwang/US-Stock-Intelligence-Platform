# US Stock Intelligence Platform



美股資料分析與投資資訊平台



## Project Overview



US Stock Intelligence Platform 是一個以 Python、Django、MySQL 建立的美股資料分析與後端資料服務專案。

系統整合外部股票 API，將每日 OHLCV 股價資料經過資料清理、驗證與轉換後寫入 MySQL，並透過 Django ORM、Pandas 與 Django REST Framework 提供股票查詢、歷史價格、資料分析與 REST API。

本專案著重於後端工程與資料流程設計，包含 JWT Authentication、Data Pipeline、Data Quality Validation、Logging、Exception Handling、Automated Tests、Docker、GitHub Actions CI 與 OpenAPI / Swagger 文件。



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
