# 📊 Avaliação de Maturidade e Compliance - TCC EJL

## 🎯 **Descrição do Projeto**

Aplicação web para avaliação do nível de compliance e maturidade da gestão de projetos de implantação de software. Desenvolvida com base em referenciais consolidados de governança e gestão de projetos (PMBOK, HCMBOK, PRINCE) e modelos de compliance.

## 🚀 **Funcionalidades**

- ✅ **Questionário Inteligente**: 10 questões distribuídas em 4 dimensões
- ✅ **Cálculo Automático**: Scores de compliance e maturidade (0-100%)
- ✅ **Sistema de Recomendações**: Sugestões baseadas em faixas de pontuação
- ✅ **Interface Responsiva**: Web app compatível com desktop e mobile
- ✅ **APIs REST**: Backend completo com Django + DRF
- ✅ **Testes Automatizados**: Suite completa de testes (16 testes passando)

## 🏗️ **Arquitetura**

- **Backend**: Django 5.2 + Django REST Framework
- **Banco de Dados**: SQLite
- **Frontend**: HTML + CSS + JavaScript (responsivo)
- **Testes**: PyTest + Django Test Framework
- **Autenticação**: Sistema de usuários Django

## 📋 **Dimensões e Questões**

### 1. **Planejamento (PMBOK)** - 3 questões
- Estrutura de governança do projeto
- Papéis e responsabilidades
- Plano de comunicação para stakeholders

### 2. **Gestão de Mudanças (HCMBOK)** - 2 questões
- Processo formal para gerenciar mudanças no escopo
- Avaliação de impacto antes da aprovação

### 3. **Qualidade (PRINCE2)** - 2 questões
- Critérios de qualidade definidos e monitorados
- Testes de software sistemáticos

### 4. **Compliance (Compliance)** - 3 questões
- Seguimento de políticas e procedimentos internos
- Registros auditáveis
- Aderência a requisitos regulatórios

## 🚀 **Como Usar**

### **Opção 1: Interface Web (Recomendado)**
1. Acesse: `http://localhost:8000/api/questionnaire/`
2. Preencha o questionário com notas de 1-5:
   - **1**: Não implementado
   - **2**: Inicial
   - **3**: Parcial
   - **4**: Implementado
   - **5**: Otimizado
3. Clique em "📋 Enviar Avaliação"
4. Visualize o relatório com scores e recomendações

### **Opção 2: APIs Diretas**
```bash
# 1. Criar projeto demo
POST /api/demo-project/
Body: {"name": "Meu Projeto"}

# 2. Enviar avaliação
POST /api/demo-assessment/
Body: {"project": 1, "answers": [{"question": 13, "value": 4}]}

# 3. Obter relatório
GET /api/demo-report/1/
```

## 🛠️ **Instalação e Configuração**

### **Pré-requisitos**
- Python 3.8+
- pip
- Git

### **Passos de Instalação**
```bash
# 1. Clone o repositório
git clone <repository-url>
cd TCC_EJLProject

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate   # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações
python manage.py migrate

# 5. Crie um superusuário (opcional)
python manage.py createsuperuser

# 6. Execute o seeder inicial
python manage.py seed_initial

# 7. Inicie o servidor
python manage.py runserver 0.0.0.0:8000
```

## 📊 **Endpoints Disponíveis**

| Endpoint | Método | Descrição | Autenticação |
|----------|--------|-----------|--------------|
| `/api/health/` | GET | Status da aplicação | ❌ |
| `/api/questionnaire/` | GET | Interface web | ❌ |
| `/api/questions/` | GET | Lista de questões | ❌ |
| `/api/dimensions/` | GET | Lista de dimensões | ❌ |
| `/api/demo-project/` | POST | Criar projeto demo | ❌ |
| `/api/demo-assessment/` | POST | Criar avaliação demo | ❌ |
| `/api/demo-report/<id>/` | GET | Relatório demo | ❌ |
| `/api/projects/` | GET/POST | Gerenciar projetos | ✅ |
| `/api/assessments/` | GET/POST | Gerenciar avaliações | ✅ |
| `/admin/` | GET | Interface administrativa | ✅ |

## 🧪 **Executando Testes**

```bash
# Executar todos os testes
python manage.py test core.tests -v 2

# Executar testes específicos
python manage.py test core.tests.CoreAPITest -v 2
python manage.py test core.tests.CoreModelsTest -v 2
```

## 🔧 **Troubleshooting**

### **Erro: "Erro ao criar projeto"**
- ✅ **Resolvido**: Endpoints demo criados para uso público
- ✅ **Status**: Funcionando perfeitamente

### **Erro: CSRF Token**
- ✅ **Resolvido**: Endpoints demo com `@csrf_exempt`
- ✅ **Status**: Funcionando perfeitamente

### **Erro: Autenticação necessária**
- ✅ **Resolvido**: Endpoints demo para uso público
- ✅ **Status**: Funcionando perfeitamente

## 📈 **Algoritmo de Scoring**

### **Compliance Score**
- Média ponderada das respostas (1-5)
- Normalizado para escala 0-100%
- Fórmula: `(média_ponderada / 5) * 100`

### **Maturity Score**
- Baseado no compliance score
- Considera consistência entre dimensões
- Mesma escala 0-100%

### **Recomendações**
- **0-40%**: Foco em implementação básica
- **41-70%**: Aprimoramento de processos
- **71-100%**: Otimização e consolidação

## 🔒 **Segurança**

- Endpoints demo são públicos para demonstração
- Endpoints principais requerem autenticação
- Proteção CSRF ativa para endpoints autenticados
- Validação de dados em todos os inputs

## 📝 **Logs e Monitoramento**

- Logs de criação de projetos demo
- Logs de avaliações realizadas
- Métricas de uso disponíveis via admin

## 🚀 **Próximos Passos**

1. **Personalizar questões** para contexto específico
2. **Ajustar pesos** conforme importância
3. **Refinar recomendações** baseadas em experiência
4. **Adicionar métricas financeiras** (se necessário)
5. **Integrar com ferramentas externas** (versões futuras)

## 📞 **Suporte**

- **Status**: ✅ Aplicação 100% funcional
- **Testes**: ✅ 16/16 testes passando
- **Endpoints**: ✅ Todos funcionando
- **Interface**: ✅ Responsiva e funcional

## 🎉 **Status Final**

**✅ DESENVOLVIMENTO CONCLUÍDO COM SUCESSO!**

A aplicação está pronta para uso e demonstração, com todas as funcionalidades implementadas e testadas.
