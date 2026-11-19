void reject(int);
int on_order(int qty, int limit) {
  if (qty > limit) {
    reject(qty);
    return -1;
  }
  return qty * 2;
}
