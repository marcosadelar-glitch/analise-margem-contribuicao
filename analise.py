import pandas as pd

df = pd.read_csv(r'D:\OneDrive\Área de Trabalho\projeto-margem-contribuicao\dataset_margem_contribuicao.csv')

print(df.head())
print(df.shape)
# Mostra os nomes de todas as colunas
print(df.columns.tolist())

# Mostra estatísticas básicas (média, mínimo, máximo) das colunas numéricas
print(df.describe())

# Mostra quais filiais existem, sem repetir
print(df['filial'].unique())
# Agrupa os dados por filial e soma receita, margem e resultado ao longo do ano todo
resumo_filial = df.groupby('filial').agg(
    receita_total=('receita', 'sum'),
    margem_total=('margem_contribuicao', 'sum'),
    resultado_total=('resultado_liquido', 'sum')
)

# Calcula o percentual de margem sobre a receita
resumo_filial['margem_pct'] = (resumo_filial['margem_total'] / resumo_filial['receita_total'] * 100).round(1)

# Ordena da pior filial (mais prejuízo) pra melhor
resumo_filial = resumo_filial.sort_values('resultado_total')

print(resumo_filial)
# Filtra só as duas piores filiais
piores_filiais = df[df['filial'].isin(['Filial Recife', 'Filial Curitiba'])]

# Agrupa por produto dentro dessas filiais, pra ver onde está o problema
resumo_produto = piores_filiais.groupby(['filial', 'produto']).agg(
    receita_total=('receita', 'sum'),
    margem_pct_media=('margem_contribuicao_pct', 'mean')
).round(3)

print(resumo_produto.sort_values('margem_pct_media'))
import matplotlib.pyplot as plt

# Pega a tabela que já calculamos (filial + produto) e "destrava" o índice duplo
# pra ficar mais fácil de plotar
grafico_dados = resumo_produto.reset_index()

# Cria uma tabela pivô: cada linha é um produto, cada coluna é uma filial,
# e o valor é a margem % média
pivot = grafico_dados.pivot(index='produto', columns='filial', values='margem_pct_media')

# Desenha um gráfico de barras comparando as duas filiais, produto a produto
pivot.plot(kind='bar', figsize=(10, 6))

plt.title('Margem de Contribuição % por Produto — Recife vs Curitiba')
plt.ylabel('Margem de Contribuição (%)')
plt.xlabel('Produto')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Filial')
plt.tight_layout()

# Salva o gráfico como imagem (fica na mesma pasta do projeto)
plt.savefig('grafico_margem_produtos.png')

# Também abre numa janela pra você ver na hora
plt.show()