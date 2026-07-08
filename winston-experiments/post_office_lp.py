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
    # Naším cílem je minimalizovat celkový součet všech najmutých pracovníků
    solver.Minimize(x1 + x2 + x3 + x4 + x5 + x6 + x7)

    # 3. OMEZUJÍCÍ PODMÍNKY (Constraints)
    solver.Add(x1 + x4 + x5 + x6 + x7 >= 17, "Poptavka_Po")
    solver.Add(x1 + x2 + x5 + x6 + x7 >= 13, "Poptavka_Ut")
    solver.Add(x1 + x2 + x3 + x6 + x7 >= 15, "Poptavka_St")
    solver.Add(x1 + x2 + x3 + x4 + x7 >= 19, "Poptavka_Ct")
    solver.Add(x1 + x2 + x3 + x4 + x5 >= 14, "Poptavka_Pa")
    solver.Add(x2 + x3 + x4 + x5 + x6 >= 16, "Poptavka_So")
    solver.Add(x3 + x4 + x5 + x6 + x7 >= 11, "Poptavka_Ne")

    # 4. VÝPOČET
    status = solver.Solve()

    # 5. VÝPIS VÝSLEDKŮ
    if status == pywraplp.Solver.OPTIMAL:
        print("=========================================")
        print(" OPTIMÁLNÍ ŘEŠENÍ NALEZENO (GLOP Solver) ")
        print("=========================================")
        print(f"Celkový počet zaměstnanců: {solver.Objective().Value():.2f}\n")

    # Týdenní náklady na práci pro porovnání s part time variantou problému
        print(f"Celkové týdenní náklady: {15 * 5 * 8 * (solver.Objective().Value()):.2f}\n")
        
        print(f"Začínají v Po (x1): {x1.solution_value():.2f}")
        print(f"Začínají v Út (x2): {x2.solution_value():.2f}")
        print(f"Začínají ve St (x3): {x3.solution_value():.2f}")
        print(f"Začínají ve Čt (x4): {x4.solution_value():.2f}")
        print(f"Začínají v Pá (x5): {x5.solution_value():.2f}")
        print(f"Začínají v So (x6): {x6.solution_value():.2f}")
        print(f"Začínají v Ne (x7): {x7.solution_value():.2f}")
    else:
        print("Řešení nebylo nalezeno. Zkontroluj si rovnice.")

if __name__ == '__main__':
    solve_post_office()