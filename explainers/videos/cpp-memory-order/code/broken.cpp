struct Msg { long price; int qty; };
Msg msg;
bool ready = false;              // plain bool: a data race

void publish(long p, int q) {    // thread 1
  msg.price = p;
  msg.qty = q;
  ready = true;
}
long consume() {                 // thread 2
  while (!ready) {}              // spin until published
  return msg.price;
}
