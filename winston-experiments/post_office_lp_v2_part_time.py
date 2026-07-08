from ortools.linear_solver import pywraplp

def solve_post_office():
    # Vytvoření solveru pro spojité lineární programování (GLOP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Chyba: Solver GLOP nebyl nalezen.")
        return
    
    # 1. ROZHODOVACÍ PROMĚNNÉ
    """ Proměnné reprezentují počet hodin, který odpracují pracovníci začínající v daný den
    za jeden pracovní den. """
    x1 = solver.NumVar(0, solver.infinity(), 'Start_Po_Full')
    x2 = solver.NumVar(0, solver.infinity(), 'Start_Ut_Full')
    x3 = solver.NumVar(0, solver.infinity(), 'Start_St_Full')
    x4 = solver.NumVar(0, solver.infinity(), 'Start_Ct_Full')
    x5 = solver.NumVar(0, solver.infinity(), 'Start_Pa_Full')
    x6 = solver.NumVar(0, solver.infinity(), 'Start_So_Full')
    x7 = solver.NumVar(0, solver.infinity(), 'Start_Ne_Full')

    y1 = solver.NumVar(0, solver.infinity(), 'Start_Po_Part')
    y2 = solver.NumVar(0, solver.infinity(), 'Start_Ut_Part')
    y3 = solver.NumVar(0, solver.infinity(), 'Start_St_Part')
    y4 = solver.NumVar(0, solver.infinity(), 'Start_Ct_Part')
    y5 = solver.NumVar(0, solver.infinity(), 'Start_Pa_Part')
    y6 = solver.NumVar(0, solver.infinity(), 'Start_So_Part')
    y7 = solver.NumVar(0, solver.infinity(), 'Start_Ne_Part')

    # 2. ÚČELOVÁ FUNKCE
    # Naším cílem je minimalizovat celkové týdenní náklady na práci
    solver.Minimize(15  * 5 * (x1 + x2 + x3 + x4 + x5 + x6 + x7) + 10 * 5 * (y1 + y2 + y3 + y4 + y5 + y6 + y7))

    # 3. OMEZUJÍCÍ PODMÍNKY (Constraints)
    solver.Add(x1 + y1 + x4 + y4 + x5 + y5 + x6 + y6 + x7 + y7 >= 136, "Poptavka_Po")
    solver.Add(x1 + y1 + x2 + y2 + x5 + y5 + x6 + y6 + x7 + y7 >= 104, "Poptavka_Ut")
    solver.Add(x1 + y1 + x2 + y2 + x3 + y3 + x6 + y6 + x7 + y7 >= 120, "Poptavka_St")
    solver.Add(x1 + y1 + x2 + y2 + x3 + y3 + x4 + y4 + x7 + y7 >= 152, "Poptavka_Ct")
    solver.Add(x1 + y1 + x2 + y2 + x3 + y3 + x4 + y4 + x5 + y5 >= 112, "Poptavka_Pa")
    solver.Add(x2 + y2 + x3 + y3 + x4 + y4 + x5 + y5 + x6 + y6 >= 128, "Poptavka_So")
    solver.Add(x3 + y3 + x4 + y4 + x5 + y5 + x6 + y6 + x7 + y7 >= 88, "Poptavka_Ne")
    solver.Add(5 * (y1 + y2 + y3 + y4 + y5 + y6 + y7) <= 210, "Max_Part_Time_Hours")

    # 4. VÝPOČET
    status = solver.Solve()

    # 5. VÝPIS VÝSLEDKŮ
    if status == pywraplp.Solver.OPTIMAL:
        print("=========================================")
        print(" OPTIMÁLNÍ ŘEŠENÍ NALEZENO (GLOP Solver) ")
        print("=========================================")
        print(f"Celkové náklady: {solver.Objective().Value():.2f}\n")

        # Zpětné odškálování na HLAVY (Full-time dělíme 8, Part-time dělíme 4)
        print("Najmout FULL-TIME zaměstnanců (začátek v daný den):")
        print(f"  Pondělí: {x1.solution_value() / 8:.2f}")
        print(f"  Úterý:   {x2.solution_value() / 8:.2f}")
        print(f"  Středa:  {x3.solution_value() / 8:.2f}")
        print(f"  Čtvrtek: {x4.solution_value() / 8:.2f}")
        print(f"  Pátek:   {x5.solution_value() / 8:.2f}")
        print(f"  Sobota:  {x6.solution_value() / 8:.2f}")
        print(f"  Neděle:  {x7.solution_value() / 8:.2f}\n")

        print("Najmout PART-TIME zaměstnanců (začátek v daný den):")
        print(f"  Pondělí: {y1.solution_value() / 4:.2f}")
        print(f"  Úterý:   {y2.solution_value() / 4:.2f}")
        print(f"  Středa:  {y3.solution_value() / 4:.2f}")
        print(f"  Čtvrtek: {y4.solution_value() / 4:.2f}")
        print(f"  Pátek:   {y5.solution_value() / 4:.2f}")
        print(f"  Sobota:  {y6.solution_value() / 4:.2f}")
        print(f"  Neděle:  {y7.solution_value() / 4:.2f}")
        
    else:
        print("Řešení nebylo nalezeno. Zkontroluj si rovnice.")

if __name__ == '__main__':
    solve_post_office()