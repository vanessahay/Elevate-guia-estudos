# ☁️ Lab 1.3: Using Antigravity to Compare an AWS Environment to Google Cloud and Generate Terraform

* **Código do Laboratório / ID**: `65280132`
* **Curso Qwiklabs**: `[ELEVATE]: Advanced Agentic AI` (Course Template: `1738435`)
* **Módulo**: Módulo 1 - Modernizing Workloads and Outage Remediation
* **Paradigma de Execução**: `Guided Procedural`
* **Quantidade de Trackers de Atividade**: 2 Activity Trackers

---

## 📋 Sumário
1. [Cenário de Migração Cross-Cloud (AWS para GCP)](#1-cenário-de-migração-cross-cloud-aws-para-gcp)
2. [Matriz de Mapeamento de Serviços (AWS vs GCP)](#2-matriz-de-mapeamento-de-serviços-aws-vs-gcp)
3. [Passo a Passo da Migração](#3-passo-a-passo-da-migração)
   - [3.1 Ingestão dos Arquivos de Configuração AWS](#31-ingestão-dos-arquivos-de-configuração-aws)
   - [3.2 Síntese do Plano de Migração com Antigravity](#32-síntese-do-plano-de-migração-com-antigravity)
   - [3.3 Geração dos Manifestos Terraform para Google Cloud](#33-geração-dos-manifestos-terraform-para-google-cloud)
   - [3.4 Validação (`terraform plan`) e Provisionamento (`terraform apply`)](#34-validação-terraform-plan-e-provisionamento-terraform-apply)
4. [Tabela de Trackers de Atividade](#4-tabela-de-trackers-de-atividade)
5. [Boas Práticas de Infraestrutura como Código (IaC)](#5-boas-práticas-de-infraestrutura-como-código-iac)

---

## 1. Cenário de Migração Cross-Cloud (AWS para GCP)

Uma organização multinacional deseja migrar uma infraestrutura de e-commerce hospedada na AWS para o **Google Cloud**, visando redução de TCO e integração com os serviços de inteligência artificial da Vertex AI.

O desafio consiste em:
- Interpretar arquivos de especificação de recursos AWS (VPC, Subnets, EC2 Instances, RDS Aurora MySQL, S3 Buckets, IAM Roles e Security Groups).
- Determinar as tecnologias equivalentes no Google Cloud que preservem os SLAs de segurança e resiliência.
- Escrever código HCL (Terraform) idiomático e modularizado para provisionamento automatizado.

---

## 2. Matriz de Mapeamento de Serviços (AWS vs GCP)

| Componente AWS | Equivalente Google Cloud | Razão da Escolha Arquitetural |
| :--- | :--- | :--- |
| **AWS VPC & Subnets** | **Google Cloud VPC (Global Subnets)** | Roteamento nativo global com subnetworks por região. |
| **AWS EC2 (Auto Scaling)** | **Managed Instance Groups (MIG)** | Escalabilidade horizontal baseada em métricas de CPU/memória. |
| **AWS RDS Aurora (MySQL)** | **Cloud SQL para MySQL / AlloyDB** | Banco relacional totalmente gerenciado com alta disponibilidade multi-zona. |
| **AWS S3 Bucket** | **Cloud Storage (GCS Standard)** | Armazenamento de objetos global com replicação geográfica e criptografia CMEK. |
| **AWS Security Groups** | **VPC Firewall Rules / Cloud Armor** | Políticas estritas de negação por padrão (*least privilege*). |

---

## 3. Passo a Passo da Migração

### 3.1 Ingestão dos Arquivos de Configuração AWS
```bash
# Navegar para o workspace e inspecionar a topologia AWS de entrada
cd ~/aws-migration
cat aws_environment.json
```

### 3.2 Síntese do Plano de Migração com Antigravity
Utilizando a persona de arquiteto de nuvem do Antigravity, o agente analisa os recursos AWS e produz uma especificação formal de migração:
```text
Prompt Antigravity:
"Analyze the AWS environment definitions in aws_environment.json. Generate a detailed Google Cloud migration plan mapping compute, networking, database, and storage resources to their GCP counterparts. Output the architecture comparison and resource sizing."
```

### 3.3 Geração dos Manifestos Terraform para Google Cloud
O Antigravity sintetiza os arquivos Terraform modulares:
- `main.tf`: Provedor Google Cloud e orquestração dos módulos.
- `vpc.tf`: Criação da rede customizada e subnets regionais.
- `compute.tf`: Definição de Compute Engine e templates de instância.
- `storage.tf`: Provisionamento de buckets GCS com controle de versão habilitado.

Exemplo de `storage.tf` gerado:
```hcl
resource "google_storage_bucket" "migrated_assets" {
  name          = "${var.project_id}-migrated-assets"
  location      = "US"
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
```

### 3.4 Validação e Provisionamento
```bash
# Inicializar o provedor Terraform
terraform init

# Validar sintaxe e gerar plano de execução
terraform plan -out=tfplan

# Aplicar e criar a infraestrutura no Google Cloud
terraform apply tfplan -auto-approve
```

---

## 4. Tabela de Trackers de Atividade

| Tracker ID | Descrição do Marco | Ação de Validação | Status |
| :---: | :--- | :--- | :---: |
| **AT 1** | *Analyze AWS environment and generate migration plan* | Síntese do relatório de compatibilidade e equivalência. | **PASSED** |
| **AT 2** | *Deploy Google Cloud reference architecture using Terraform* | Execução com sucesso do `terraform apply` com recursos criados. | **PASSED** |

---

## 5. Boas Práticas de Infraestrutura como Código (IaC)

1. **State Remoto Seguro**: Em produção, armazene o `terraform.tfstate` em um bucket GCS dedicado com versionamento e criptografia ativados.
2. **Princípio do Menor Privilégio**: Associe Contas de Serviço customizadas aos recursos criados, evitando a Conta de Serviço padrão de computação com permissões excessivas de editor.
