export function formatCurrency(value) {
  const amount = Number(value)

  return (Number.isFinite(amount) ? amount : 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  })
}
