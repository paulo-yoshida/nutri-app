# nutri-app
## Épico 1: Gestão de Pacientes
Este épico foca em todo o ciclo de vida do paciente dentro da clínica, desde o seu cadastro até o acompanhamento contínuo.

### Estória 1.1: Cadastro de Novo Paciente

Como uma nutricionista, eu quero cadastrar um novo paciente inserindo suas informações pessoais (nome, data de nascimento, contato), histórico clínico (patologias, alergias, medicamentos em uso) e objetivos iniciais, para que eu tenha um registro centralizado e completo desde a primeira consulta.

### Estória 1.2: Registro de Consulta de Acompanhamento

Como uma nutricionista, eu quero acessar o perfil de um paciente existente e adicionar um novo registro de consulta, incluindo a data, peso atual, novas medidas antropométricas e anotações subjetivas (como dificuldades e sucessos), para que eu possa acompanhar sua evolução ao longo do tempo.

### Estória 1.3: Visualização do Histórico do Paciente

Como uma nutricionista, eu quero visualizar um painel com o histórico de todas as consultas de um paciente, com gráficos mostrando a evolução do peso, medidas e percentual de gordura, para que eu possa analisar o progresso de forma rápida e mostrá-lo visualmente ao paciente.

## Épico 2: Avaliação da Composição Corporal
O foco aqui é automatizar os cálculos que hoje podem ser manuais e demorados, garantindo precisão e agilidade.

### Estória 2.1: Cálculo do Percentual de Gordura

Como uma nutricionista, eu quero inserir as medidas das dobras cutâneas (ex: tríceps, subescapular, suprailíaca, etc.) de um paciente, para que a ferramenta calcule automaticamente o percentual de gordura usando um protocolo científico (ex: Pollock de 7 dobras).

### Estória 2.2: Seleção de Protocolo de Cálculo

Como uma nutricionista, eu quero poder escolher entre diferentes protocolos de cálculo de percentual de gordura (ex: Pollock 3 dobras, Pollock 7 dobras, Durnin & Womersley), para que eu possa usar o método mais adequado para o perfil de cada paciente (homem, mulher, atleta, etc.).

## Épico 3: Cálculo de Necessidades Energéticas (GET)
Esta parte da ferramenta cuida de um dos cálculos mais fundamentais para a criação de um plano alimentar.

### Estória 3.1: Cálculo do Gasto Energético Total (GET)

Como uma nutricionista, eu quero inserir os dados do paciente (idade, sexo, peso, altura) e seu nível de atividade física, para que a ferramenta calcule automaticamente sua Taxa Metabólica Basal (TMB) e seu Gasto Energético Total (GET).

### Estória 3.2: Definição de Objetivo Calórico

Como uma nutricionista, eu quero, a partir do GET calculado, poder definir um objetivo (ex: perda de peso, manutenção, ganho de massa) e aplicar um ajuste calórico (ex: déficit de 500 kcal), para que a ferramenta me apresente a meta de calorias e macronutrientes para o plano alimentar.

### Estória 3.3: Seleção da Equação de Cálculo

Como uma nutricionista, eu quero poder selecionar a equação para o cálculo da TMB (ex: Harris-Benedict, Mifflin-St Jeor, FAO/OMS), para que eu possa utilizar a fórmula que considero mais precisa e atualizada.

## Épico 4: Montagem de Planos Alimentares
Este é o coração da ferramenta, onde a nutricionista aplica seu conhecimento para criar cardápios personalizados de forma eficiente.

### Estória 4.1: Busca de Alimentos na Tabela TACO

Como uma nutricionista, eu quero buscar alimentos na base de dados da Tabela TACO pelo nome, para que eu possa encontrá-los rapidamente e ver suas informações de calorias e macronutrientes (proteínas, carboidratos, gorduras).

### Estória 4.2: Construção do Cardápio Diário

Como uma nutricionista, eu quero montar um cardápio estruturado por refeições (ex: Café da Manhã, Lanche, Almoço, Jantar) e adicionar alimentos com suas respectivas quantidades (em gramas ou medidas caseiras), para que eu possa construir um plano alimentar detalhado.

### Estória 4.3: Controle em Tempo Real de Metas

Como uma nutricionista, eu quero, enquanto monto o cardápio, visualizar um resumo em tempo real do total de Kcal e da distribuição de macronutrientes, comparando com a meta definida para o paciente, para que eu possa fazer ajustes imediatos e garantir que o plano esteja adequado.

### Estória 4.4: Criação de Listas de Substituição

Como uma nutricionista, eu quero poder criar uma lista de alimentos substitutos equivalentes para cada item do plano alimentar, para que o paciente tenha mais flexibilidade e adesão à dieta.

### Estória 4.5: Geração do Plano para o Paciente

Como uma nutricionista, eu quero gerar uma versão final do plano alimentar (em PDF para impressão ou envio digital), com uma formatação clara e profissional, incluindo o cardápio, as listas de substituições e recomendações gerais, para que eu possa entregar um material de alta qualidade ao meu paciente.
