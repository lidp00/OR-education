from ortools.linear_solver import pywraplp

def solve_bank_one():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # 1. ROZHODOVACÍ PROMĚNNÉ
    # x[0] = 10-18, x[1] = 11-19, x[2] = 12-20 (směny full-time pracovníků)
    x = [solver.NumVar(0, solver.infinity(), f'x_{i}') for i in range(3)]
    
    # y[0] = 14-19, y[1] = 15-20 (směny part-time pracovníků)
    y = [solver.NumVar(0, solver.infinity(), f'y_{i}') for i in range(2)]
    
    # z[0] až z[9] reprezentují počet aktivních pracovníků v každé hodině od 10 AM do 7 PM
    z = [solver.NumVar(0, 13, f'z_{i}') for i in range(10)]

    # 2. ÚČELOVÁ FUNKCE (Minimalizace nákladů)
    solver.Minimize(160 * sum(x) + 75 * sum(y))

    # 3. OMEZUJÍCÍ PODMÍNKY
    
    # Globální pravidlo managementu: alespoň 3 full-time
    solver.Add(sum(x) >= 3, "Min_Full_Time")

    # A) Kumulativní logika šeků
    incoming_checks = [5000, 4000, 3000, 4000, 2500, 3000, 4000, 4500, 3500, 3000]
    cumulative_checks = [sum(incoming_checks[:i+1]) for i in range(10)]
    
    for i in range(9): # Od 10 AM do 6 PM (posunutí kapacity nesmí překročit to, co dosud přišlo)
        solver.Add(500 * sum(z[:i+1]) <= cumulative_checks[i])
        
    # V 7 PM musí být odbaveno vše (tvrdé rovnítko na konci směny)
    solver.Add(500 * sum(z) == cumulative_checks[9])

    # B) Rozpis přítomných pracovníků podle hodin
    active_workers = [
        [x[0]],                            # 10 AM
        [x[0], x[1]],                      # 11 AM
        [x[0], x[1], x[2]],                # Noon
        [x[0], x[1], x[2]],                # 1 PM
        [x[0], x[1], x[2], y[0]],          # 2 PM
        [x[0], x[1], x[2], y[0], y[1]],    # 3 PM
        [x[0], x[1], x[2], y[0], y[1]],    # 4 PM
        [x[0], x[1], x[2], y[0], y[1]],    # 5 PM
        [x[1], x[2], y[0], y[1]],          # 6 PM
        [x[2], y[1]]                       # 7 PM
    ]
    
    # Počet aktivních pracovníků v danou hodinu nesmí převýšit celkový počet přítomných pracovníků
    for i in range(10):
        solver.Add(z[i] <= sum(active_workers[i]))

    # 4. VÝPOČET
    status = solver.Solve()

    # 5. VÝPIS VÝSLEDKŮ
    if status == pywraplp.Solver.OPTIMAL:
        print("=========================================")
        print(" OPTIMÁLNÍ ROZVRH NALEZEN (GLOP) ")
        print("=========================================")
        print(f"Minimální denní náklady: ${solver.Objective().Value():.2f}\n")
        
        print("--- ZAMĚSTNANCI ---")
        print(f"Full-time (10-18): {abs(x[0].solution_value()):.2f} lidí")
        print(f"Full-time (11-19): {abs(x[1].solution_value()):.2f} lidí")
        print(f"Full-time (12-20): {abs(x[2].solution_value()):.2f} lidí")
        print(f"Part-time (14-19): {abs(y[0].solution_value()):.2f} lidí")
        print(f"Part-time (15-20): {abs(y[1].solution_value()):.2f} lidí\n")
        
        print("--- AKTIVNÍ PRACOVNÍCI ---")
        print("Každý pracovník zvládne obsluhovat 1 stroj, tedy 500 šeků za hodinu.")
        print("Banka má k dispozici 13 strojů, tedy maximálně 13 pracovníků může být aktivních v danou hodinu.")
        cas = 10
        for i in range(10):
            print(f"{cas}:00 -> Aktivních {z[i].solution_value():.2f} pracovníků.")
            cas += 1
    else:
        print("Řešení nebylo nalezeno.")

if __name__ == '__main__':
    solve_bank_one()