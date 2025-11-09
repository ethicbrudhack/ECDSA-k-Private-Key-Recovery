def modinv(a, n):
    """
    Oblicza modularny odwrotność liczby a modulo n.
    Zwraca x takie, że (a * x) % n == 1.
    Jeśli odwrotność nie istnieje, zgłasza wyjątek.
    """
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError(f"Odwrotność modulo nie istnieje dla {a} mod {n}")
    if t < 0:
        t += n
    return t

def compute_private_key(z1, z2, r1, r2, s1, s2, delta_k, n):
    """
    Oblicza prywatny klucz d według wzoru:
    
      d = [Δk * s1 * s2 - (s2*z1 - s1*z2)] * (s2*r1 - s1*r2)^{-1} mod n
      
    Argumenty:
      z1, z2: skróty (hash) wiadomości podpisywanych
      r1, r2: wartość r z podpisów
      s1, s2: wartość s z podpisów
      delta_k: różnica k1 - k2
      n: moduł (np. rząd grupy w ECDSA)
      
    Zwraca:
      Prywatny klucz d (liczbę całkowitą)
    """
    numerator = (delta_k * s1 * s2 - (s2 * z1 - s1 * z2)) % n
    denominator = (s2 * r1 - s1 * r2) % n
    inv_denominator = modinv(denominator, n)
    d = (numerator * inv_denominator) % n
    return d

def compute_ephemeral_key(z, r, s, d, n):
    """
    Oblicza ephemeralny klucz k według wzoru:
    
      k = (z + d * r) * s^{-1} mod n
      
    Argumenty:
      z: skrót podpisywanej wiadomości
      r: wartość r z podpisu
      s: wartość s z podpisu
      d: prywatny klucz
      n: moduł
      
    Zwraca:
      ephemeralny klucz k
    """
    inv_s = modinv(s, n)
    k = (z + d * r) * inv_s % n
    return k

def main():
    # Przykładowe dane (należy je podmienić na właściwe wartości)
    z1 = 46159134511846639653039227807867168677952429760806101162575716914492122120852
    z2 = 7519772703183545940918986660617875086369147038649256132503899290067419860069
    r1 = 96305888925087028226280700902788330707257073607110099029890896029884121755055
    r2 = 111616838599096250300489315075857406212435899769031134709979742002100806022869
    s1 = 16473844652988003574805773187527026768208893032028674194682143648834372476120
    s2 = 82526933124808898216141238576469063794369340677613970807733221005881288311205
    
    # Różnica między ephemeralnymi kluczami: Δk = k1 - k2
    delta_k = 3141592653589793  # przykładowa wartość, do zastąpienia
    
    # Moduł n (np. rząd grupy w używanym systemie ECDSA)
    n = 0xfffffffffffffffffffffffe26f2fc170f69466a74defd8d  # przykładowy moduł, należy podać właściwy
    
    try:
        d = compute_private_key(z1, z2, r1, r2, s1, s2, delta_k, n)
        k1 = compute_ephemeral_key(z1, r1, s1, d, n)
        k2 = compute_ephemeral_key(z2, r2, s2, d, n)
        
        print("Prywatny klucz d =", d)
        print("Ephemeralny klucz k1 =", k1)
        print("Ephemeralny klucz k2 =", k2)
        print("Różnica k1 - k2 =", (k1 - k2) % n)
    except ValueError as e:
        print("Wystąpił błąd:", e)

if __name__ == '__main__':
    main()

