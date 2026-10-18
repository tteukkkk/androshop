# Revisão para portfólio

## Alterações comuns

- Removidos ambientes virtuais, arquivos compilados, bancos SQLite, uploads locais e estáticos coletados.
- Configuração de credenciais por variáveis de ambiente; arquivo `.env.example` sem senha real.
- SQLite como padrão para demonstração e MySQL opcional.
- Dependências e instruções de instalação documentadas.
- DEFAULT_AUTO_FIELD alinhado às migrações existentes.

## Alterações específicas

Quantidade inválida tratada no carrinho; checkout atômico com bloqueio de produtos e verificação de estoque. Cálculo de desconto limitado a 0–100%.

## Verificação executada

Python 3.12.14 / Django 5.2.18 / SQLite. 4 testes passaram; check, conferência de migrações e migrate concluíram com sucesso. Testes novos cobrem fluxos alterados e se somam aos testes originais. Não houve teste de MySQL, concorrência real, implantação ou inspeção visual em navegador da aplicação local.

## Limitações

Não há cobrança real: a confirmação de pagamento altera apenas o status local. A versão de estudo ainda não implementa frete, cancelamento com estorno de estoque ou integração com gateway. Os testes de estoque foram executados em SQLite, não sob concorrência MySQL.

## Modelos principais

- `Categoria`
- `Produto`
- `Avaliacao`
- `CupomDesconto`
- `Pedido`
- `ItemPedido`
