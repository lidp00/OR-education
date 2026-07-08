from ortools.linear_solver import pywraplp

def solve_post_office():
    # Vytvoření solveru pro spojité lineární programování (GLOP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Chyba: Solver GLOP nebyl nalezen.")
        return
    
    # 1. ROZHODOVACÍ PROMĚNNÉ
    # Proměnné reprezentují POČET LIDÍ, kteří ZAHÁJÍ svou 5denní směnu v daný den.
    x1 = solver.NumVar(0, solver.infinity(), 'Start_Po')
    x2 = solver.NumVar(0, solver.infinity(), 'Start_Ut')
    x3 = solver.NumVar(0, solver.infinity(), 'Start_St')
    x4 = solver.NumVar(0, solver.infinity(), 'Start_Ct')
    x5 = solver.NumVar(0, solver.infinity(), 'Start_Pa')
    x6 = solver.NumVar(0, solver.infinity(), 'Start_So')
    x7 = solver.NumVar(0, solver.infinity(), 'Start_Ne')

    # 2. ÚČELOVÁ FUNKCE
    # Naším cílem je maximalizovat celkový počet volných víkendových dní.
    solver.Maximize(2 * x1 + x2 + x7)

    # 3. OMEZUJÍCÍ PODMÍNKY (Constraints)
    solver.Add(x1 + x4 + x5 + x6 + x7 >= 17, "Poptavka_Po")
    solver.Add(x1 + x2 + x5 + x6 + x7 >= 13, "Poptavka_Ut")
    solver.Add(x1 + x2 + x3 + x6 + x7 >= 15, "Poptavka_St")
    solver.Add(x1 + x2 + x3 + x4 + x7 >= 19, "Poptavka_Ct")
    solver.Add(x1 + x2 + x3 + x4 + x5 >= 14, "Poptavka_Pa")
    solver.Add(x2 + x3 + x4 + x5 + x6 >= 16, "Poptavka_So")
    solver.Add(x3 + x4 + x5 + x6 + x7 >= 11, "Poptavka_Ne")
    solver.Add(x1 + x2 + x3 + x4 + x5 + x6 + x7 == 25, "Pocet_zamestnancu")

    # 4. VÝPOČET
    status = solver.Solve()

    # 5. VÝPIS VÝSLEDKŮ
    if status == pywraplp.Solver.OPTIMAL:
        print("=========================================")
        print(" OPTIMÁLNÍ ŘEŠENÍ NALEZENO (GLOP Solver) ")
        print("=========================================")
        print(f"Celkový počet volných víkendových dní: {solver.Objective().Value():.2f}\n")
    else:
        print("Řešení nebylo nalezeno.")

if __name__ == '__main__':
    solve_post_office()