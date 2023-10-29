# mqtt
Network project

## sources

https://github.com/eclipse/paho.mqtt.python

## checklist

1. Descrever o projeto do sistema, contemplando a arquitetura do sistema e a definição e formato dos tópicos de controle para comunicação um-a-um e em grupo.

2. Implementação da aplicação:

▪ Listagem dos usuários e seus respectivos status (online/offline);

▪ Criação de grupo (caso o grupo não exista, o criador do grupo se autodeclara líder do mesmo).
▪ Listagem dos grupos cadastrados: para cada grupo, listar o nome do grupo, líder e demais membros;

▪ Solicitação de conversa 

▪ Listagem do histórico de solicitação recebidas
▪ Listagem das confirmações de aceitação da solicitação de batepapo + informação do tópico criado para iniciar o bate-papo.

## requesitos

Comunicação um-a-um (one-to-one) e comunicação em grupo
◦ Identificadores de usuários (ID) são únicos;
◦ Assumir que usuários conhecem o ID dos demais usuários.
• Modo de comunicação: comunicação com usuários online com persitência de dados para usuários offline.

Há um tópico para interação de controle com cada cliente: ID_Control
◦ Exemplo: para um usuário com ID = X o tópico será X_Control
◦ Cada cliente assina e publica no seu próprio tópico de controle (os demais só podem publicar).
◦ Solicitação/negociação de uma nova sessão (conversation) deve ser via o canal de
controle: cada sessão deve ter, para o mesmo par de usuários, um identificador único.
▪ Ao aceitar a solicitação, o usuário solicitado define um tópico com o mesmo nome
correspondente ao identificador da sessão. Exemplo: assumindo que Y quer falar
com X, o nome do tópico pode ser X_Y_timestamp (timestamp pode ser o horário
atual de início do bate-papo).
▪ O identificador da sessão (nome do novo tópico) é comunicado ao solicitante via
publicação no seu tópico de cliente (i.e., publish to ID_Cliente). No exemplo
anterior, X publicaria no tópico de Y (ou seja, Y_Control).

Definir um tópico de controle USERS onde são publicados o status (online ou offline) de
cada usuário. Assumir que cada usuário comunica seu estado online ao iniciar o aplicativo, e
o estado offline antes de encerrar o aplicativo.

Definir um tópico de controle GROUPS onde são publicadas informações de cada grupo:
nome do grupo, nome do usuário que é líder do grupo e lista dos demais membros. A
solicitação de ingresso a um grupo deve ser dirigida ao líder que, após aceitar, atualiza a
informação do grupo via publicação no tópico GROUPS.
