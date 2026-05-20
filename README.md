# Sistema de Chamados Acadêmicos — Projeto de Arquitetura em Nuvem

Este projeto apresenta uma proposta de arquitetura em nuvem para um sistema de chamados acadêmicos.

## Objetivo

Projetar uma solução em nuvem para uma instituição de ensino que precisa organizar chamados técnicos de laboratórios de informática.

## Principais componentes

- Aplicação Web
- API Backend
- Banco de Dados Relacional
- Storage de Anexos
- Fila de Mensagens
- Worker de Notificações
- Cofre de Segredos
- Logs e Monitoramento
- Backup

## Provedores analisados

- Microsoft Azure
- Amazon Web Services
- Google Cloud

## Solução final escolhida

A solução final escolhida foi baseada no Google Cloud, utilizando Cloud Run, Cloud SQL, Cloud Storage, Pub/Sub, Secret Manager, IAM e Cloud Logging.

## Justificativa

A escolha foi feita por simplicidade, escalabilidade e facilidade de explicar uma arquitetura moderna baseada em serviços gerenciados.
