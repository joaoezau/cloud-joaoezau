# Leonida Poster — Plano

Site que transforma a foto do usuário em um pôster no estilo das artes de capa de jogos de mundo aberto (neon, palmeiras, pintura digital, clima de Miami). Modelo inspirado no Fable: **prévia grátis, paga só se gostar.**

---

## 1. Como funciona para o usuário

1. Entra no site e vê exemplos de pôsteres.
2. Envia uma foto (de si mesmo, de um amigo, de um casal, de um pet).
3. Escolhe um estilo.
4. Espera cerca de 1 minuto, vendo uma animação de progresso.
5. Recebe a **prévia com marca d'água e em baixa resolução**, de graça e sem cadastro.
6. Se gostar, paga e baixa a versão em HD, sem marca d'água.
7. Se não gostar, tenta outro estilo ou outra foto, dentro do limite grátis.

## 2. Telas

| Tela | O que tem |
|---|---|
| **Início** | Título, galeria de exemplos, botão "Criar meu pôster", perguntas frequentes |
| **Criar** | Upload da foto, dicas de foto boa, escolha do estilo |
| **Gerando** | Animação de progresso (cerca de 1 minuto) |
| **Resultado** | Prévia com marca d'água, botões "Comprar HD" e "Tentar outro estilo" |
| **Pagamento** | Checkout do Mercado Pago (Pix e cartão) |
| **Download** | Link para baixar o HD; esse link também vai para o e-mail |
| **Privacidade / Termos** | Página exigida pela LGPD e pelo Mercado Pago |

## 3. Estilos iniciais

1. **Capa** — a pessoa como destaque de uma arte de capa, em painel, com pôr do sol neon
2. **Personagem** — retrato de corpo inteiro com pose, sobre fundo de cor chapada
3. **Noite neon** — cena noturna de cidade, com carro e luzes rosa e azul
4. **Praia** — palmeiras, mar, conversível, luz dourada

Os prompts descrevem só a estética: **nada de "GTA", "Rockstar", logos ou personagens.**

## 4. Tecnologia

| Parte | Escolha | Por quê |
|---|---|---|
| Site | **Next.js** na **Vercel Pro** | O plano grátis da Vercel não permite uso comercial |
| IA | **FLUX Kontext** no **fal.ai** ou no **Replicate** | Transforma foto em estilo e não barra estilo artístico |
| Estilo | **LoRA** de estilo treinado com ~20 a 30 artes de referência (**decidido: Opção A**) | Deixa o resultado com cara de "capa de jogo" |
| Fundos | **Camadas próprias** (céus, palmeiras, praias, cidade) geradas com o LoRA | Toda a arte do pôster é original; só a pessoa é gerada na hora |
| Marca d'água e redução | **sharp**, no servidor | O HD nunca vai para o navegador antes do pagamento |
| Armazenamento | **Supabase Storage** ou **Cloudflare R2**, em pasta privada | O HD fica guardado até o pagamento ser aprovado |
| Banco de dados | **Supabase** (Postgres) | Guarda os pedidos: status, estilo, pago ou não |
| Pagamento | **Mercado Pago**, Checkout Pro | Pix e cartão; o webhook libera o download |
| Limite grátis | **Upstash Redis** | 3 prévias por IP por dia |
| Anti-robô | **Cloudflare Turnstile** | Impede robôs de gastar seus créditos |
| E-mail | **Resend** | Envia o link do HD |

## 5. Fluxo técnico

```
Foto ──► /api/gerar ──► (checa limite + Turnstile) ──► IA (FLUX Kontext)
                                                          │
                       guarda HD privado ◄────────────────┘
                       gera prévia com marca d'água ──► mostra ao usuário

Comprar ──► Mercado Pago ──► webhook /api/pagamento ──► marca pedido como pago
                                                       └──► libera link do HD (expira em 7 dias)
```

- Cada pedido tem um ID aleatório, e o link de download só funciona com esse ID e com o pedido pago.
- As fotos enviadas são **apagadas em 48h**; o HD é apagado em 30 dias.

## 6. Preços sugeridos

| Produto | Preço | Custo |
|---|---|---|
| Prévia | Grátis (3 por dia) | ~R$0,22 de IA cada |
| HD digital | **R$9,90** | Taxa do Pix ~1% + IA |
| Pacote com 3 estilos em HD | **R$19,90** | — |

Uma venda de R$9,90 cobre cerca de 40 prévias grátis.

## 7. Custos para começar

| Item | Valor |
|---|---|
| Domínio | ~R$40 a R$80 por ano |
| Vercel Pro | ~R$110 por mês |
| Créditos de IA para testes | ~R$60 |
| Supabase, Upstash, Resend, Turnstile | Grátis no começo |
| **Total no 1º mês** | **~R$220 a R$250** |

Configure um **limite de gasto** no fal.ai ou no Replicate desde o primeiro dia.

## 8. Fases

**Fase 1 — Treinar e testar o estilo (1 a 2 dias)**
- Separar 20 a 30 artes de referência (personagens e cenas completas)
- Escrever legendas descrevendo só o estilo, sem nomes de personagens ou marcas
- Treinar o LoRA (~US$2 a US$5) e testar com 10 a 20 fotos reais
- As artes de referência ficam **fora do GitHub** e nunca aparecem no site
- Gerar o primeiro pacote de fundos em camadas

**Fase 2 — Site funcionando, sem pagamento (3 a 5 dias)**
- Telas Início, Criar, Gerando e Resultado
- Geração, marca d'água, limite por IP, Turnstile
- Mostrar para amigos e coletar opiniões

**Fase 3 — Cobrança (2 a 3 dias)**
- Mercado Pago, webhook, página de download, e-mail
- Páginas de privacidade e termos
- Lançar

**Fase 4 — Crescer**
- Novos estilos e camadas de fundo
- Pacotes de presente (casal, família, galera) e datas especiais
- Vídeo curto de "antes e depois" para TikTok e Reels

## 9. Riscos

| Risco | Como evitar |
|---|---|
| Conta da IA explodir | Limite de gasto na API, 3 prévias por IP, Turnstile |
| Marca registrada | Não usar "GTA", "Rockstar", logos nem personagens. **"Leonida" é o estado fictício do GTA 6**: se o site crescer e cobrar, considere trocar o nome |
| Fotos de outras pessoas | Termos dizendo que o usuário precisa ter autorização; filtro de nudez da API ligado |
| LGPD | Apagar fotos em 48h, página de privacidade clara |

## 10. Decisões ainda abertas

- [ ] fal.ai ou Replicate (decidir na Fase 1, testando os dois)
- [ ] Nome final do site e domínio
- [ ] Preço final do HD
