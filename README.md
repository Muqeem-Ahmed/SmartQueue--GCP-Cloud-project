# SmartQueue: Cloud-Native Patient Queue Management System

**CE-308: Cloud Computing Project** **Institution:** Ghulam Ishaq Khan Institute of Engineering Sciences and Technology (GIKI)  
**Team:** Muqeem Ahmed Soomro | Sarosh Ishaq 

---

## 📌 Project Overview
SmartQueue is a highly available, distributed cloud application built entirely on the Google Cloud Platform (GCP). It is designed to manage hospital patient queues in real-time. 

In a distributed microservices environment, keeping the user interface synced across multiple load-balanced servers is a major challenge. SmartQueue solves this by decoupling the application memory and deploying an internal **Redis database** as the single source of truth. Additionally, the system features a fully automated data pipeline that streams queue events into a data lake for real-time analytics.

## 🏗️ System Architecture
The application is fully containerized and orchestrated using **Google Kubernetes Engine (GKE) Autopilot**. 

1. **Compute Layer:** A containerized Flask Python application deployed across multiple replica pods, sitting behind a GCP External Load Balancer.
2. **State Synchronization:** An internal Redis database deployed within the Kubernetes cluster prevents state fragmentation and syncs the Patient and Admin portals instantly.
3. **Analytics Pipeline:** A Python simulator generates synthetic hospital traffic, streaming JSON logs directly into **Google Cloud Storage**. **BigQuery** queries this data serverlessly (schema-on-read), feeding a live **Looker Studio** dashboard to visualize wait times and department bottlenecks.

## 📂 Repository Structure

This repository contains two main components:

* `/smartqueue-api`
    * Contains the core Flask web application.
    * The `Dockerfile` used to containerize the application.
    * The Kubernetes YAML configuration files (`deployment.yaml`, `redis.yaml`, etc.) used to spin up the load balancer, replica pods, and Redis database.
* `/smartqueue-simulator`
    * Contains the `simulator.py` script.
    * Acts as a background service to simulate high-volume hospital traffic and upload synthetic JSON queue events to the GCP Data Lake.

## 🚀 Key Cloud Concepts Demonstrated
* **Microservices & Containerization:** Dockerizing a Python web application.
* **State Management:** Solving distributed memory issues using Redis.
* **High Availability & Load Balancing:** Distributing traffic across multiple pods.
* **Resilience & Self-Healing:** Utilizing Kubernetes to automatically detect and replace crashed pods with zero data loss.
* **Data Lakes & Analytics:** Streaming unstructured data into Cloud Storage and using BigQuery for visualization. 

## 🎥 Demonstration Highlights
During our final presentation, we demonstrated the system's resilience by manually simulating a fatal server crash (deleting an active API pod). The GCP External Load Balancer instantly routed traffic, and Kubernetes automatically spun up a replacement pod in seconds, with zero queue data lost thanks to the decoupled Redis state.
