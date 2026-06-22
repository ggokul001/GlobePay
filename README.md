# GlobePay 🌍💳

## Overview

GlobePay is a traveler-centric fintech application that helps international travelers make payments in their home currency while traveling abroad.

Users can scan merchant QR codes, view real-time exchange rates, and complete payments using their existing cards or bank accounts. Merchants receive payments in their local currency through existing payment networks.

The goal of GlobePay is to simplify cross-border payments and improve transparency for travelers.

---

## Problem Statement

International travelers often face:

* Unclear currency conversion rates
* Hidden forex fees
* Confusing payment experiences
* Difficulty understanding the actual amount being charged

GlobePay aims to solve these challenges by providing transparent currency conversion and a seamless payment experience.

---

## Key Features

### User Management

* User Registration
* Secure Login
* JWT Authentication
* Session Management

### Payment Management

* Link Payment Methods
* Manage Cards and Accounts
* Secure Payment Processing

### QR Payments

* Scan Merchant QR Codes
* Extract Merchant Information
* Validate QR Data

### Forex Services

* Live Exchange Rate Retrieval
* Currency Conversion
* Transparent Fee Calculation

### Transactions

* Initiate Payments
* Track Payment Status
* Transaction History
* Digital Receipts

### Notifications

* Payment Alerts
* Transaction Updates
* Security Notifications

### Security

* Role-Based Access Control (RBAC)
* Audit Logging
* Secure Token Management
* Encrypted Communication

---

## System Architecture

```text
Mobile App (React Native)
            │
            ▼
        API Gateway
            │
            ▼
      FastAPI Backend
            │
 ┌──────────┼──────────┐
 │          │          │
 ▼          ▼          ▼
PostgreSQL Redis External APIs

          ┌───────────────┐
          │ Forex Provider│
          ├───────────────┤
          │ Payment Provider
          ├───────────────┤
          │ Notification Provider
          └───────────────┘
```

---

## Technology Stack

### Frontend

* React Native
* TypeScript

### Backend

* Python
* FastAPI

### Database

* PostgreSQL

### Cache

* Redis

### Authentication

* JWT

### Infrastructure

* Docker
* GitHub Actions
* AWS

### Monitoring

* Prometheus
* Grafana

---

## Project Deliverables

### Requirements Engineering

* Software Requirements Specification (SRS)

### Business Analysis

* Use Case Diagram
* System Context Diagram
* Data Flow Diagrams

### Database Design

* Entity Relationship Diagram (ERD)
* Data Dictionary

### API Design

* API Requirement Specification

### Architecture Design

* High Level Design (HLD)
* Low Level Design (LLD)

---

## Project Goals

* Support millions of users
* Follow production-grade architecture principles
* Demonstrate real-world fintech system design
* Showcase scalability, security, and reliability
* Build a FAANG-level portfolio project

---

## Future Enhancements

* Multi-country QR Standards
* Advanced Fraud Detection
* AI-Based Spending Insights
* Multi-Language Support
* Offline Transaction Queue
* Merchant Analytics

---

## Status

Current Phase:

System Design & Architecture

Progress:

* Requirements Engineering ✅
* Business Modeling ✅
* Database Design ✅
* API Design 🚧
* Development ⏳
* Testing ⏳
* Deployment ⏳

---

## Author

Gokulakrishnan G

Computer Science and Engineering Student

Passionate about FinTech, Cybersecurity, System Design, and Scalable Software Engineering.
