from ortools.linear_solver import pywraplp

def solve_paynothing_shoes():
    # Použití GLOP řešiče pro lineární programování
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # 1. ROZHODOVACÍ PROMĚNNÉ
    # Pracovníci začínající v daném kvartálu
    # x[0] = x_1 (1. kvartál), x[1] = x_2 (2. kvartál), x[2] = x_3 (3. kvartál), x[3] = x_4 (4. kvartál)
    x = [solver.NumVar(0, solver.infinity(), f'x_{i+1}') for i in range(4)]
    
    # Zásoby bot na začátku kvartálu (resp. na konci předchozího)
    # i[0] = i_2 (začátek 2. Q), i[1] = i_3 (začátek 3. Q), i[2] = i_4 (začátek 4. Q)
    # i_1 je dle zadání rovno 0
    i = [solver.NumVar(0, solver.infinity(), f'i_{k+2}') for k in range(3)]

    # 2. ÚČELOVÁ FUNKCE (Minimalizace ročních nákladů)
    # $1500 za každého pracovníka (500 za každý z jeho 3 pracovních kvartálů)
    # $50 za uskladnění každého páru bot na konci kvartálu
    solver.Minimize(1500 * sum(x) + 50 * sum(i))

    # 3. OMEZUJÍCÍ PODMÍNKY (Bilanční rovnice kvartálů)
    
    # 1. kvartál: Pracují x_1, x_3, x_4. Produkce - zásoby_konec(i_2) = poptávka
    solver.Add(50 * (x[0] + x[2] + x[3]) - i[0] == 600, "Kvartal_1")
    
    # 2. kvartál: Pracují x_1, x_2, x_4. Produkce + zásoby_zacatek(i_2) - zásoby_konec(i_3) = poptávka
    solver.Add(50 * (x[0] + x[1] + x[3]) + i[0] - i[1] == 300, "Kvartal_2")
    
    # 3. kvartál: Pracují x_1, x_2, x_3. Produkce + zásoby_zacatek(i_3) - zásoby_konec(i_4) = poptávka
    solver.Add(50 * (x[0] + x[1] + x[2]) + i[1] - i[2] == 800, "Kvartal_3")
    
    # 4. kvartál: Pracují x_2, x_3, x_4. Produkce + zásoby_zacatek(i_4) = poptávka (zásoby na konci roku jsou 0)
    solver.Add(50 * (x[1] + x[2] + x[3]) + i[2] == 100, "Kvartal_4")


    # 4. VÝPOČET
    status = solver.Solve()

    # 5. VÝPIS VÝSLEDKŮ
    if status == pywraplp.Solver.OPTIMAL:
        print("=========================================")
        print(" OPTIMÁLNÍ PLÁN NALEZEN (GLOP) ")
        print("=========================================")
        print(f"Minimální roční náklady: ${solver.Objective().Value():.2f}\n")
        
        print("--- ZAMĚSTNANCI ---")
        print("Rotace: Zaměstnanec pracuje 3 kvartály a pak má 1 kvartál volno.")
        for j in range(4):
            print(f"Skupina začínající v {j+1}. kvartálu (x_{j+1}): {abs(x[j].solution_value()):.2f} lidí")
            
        print("\n--- ZÁSOBY NA KONCI KVARTÁLU ---")
        print(f"Konec 1. kvartálu (i_2): {abs(i[0].solution_value()):.2f} párů bot")
        print(f"Konec 2. kvartálu (i_3): {abs(i[1].solution_value()):.2f} párů bot")
        print(f"Konec 3. kvartálu (i_4): {abs(i[2].solution_value()):.2f} párů bot")
        print("Konec 4. kvartálu:       0.00 párů bot (dle definice)\n")
    else:
        print("Řešení nebylo nalezeno.")

if __name__ == '__main__':
    solve_paynothing_shoes()