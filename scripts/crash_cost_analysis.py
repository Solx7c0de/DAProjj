def run_crash_analysis(df):
    df = df.copy()
    df = df[df['Slack'] == 0].copy()
    df['CrashCostPerDay'] = (df['CrashCost'] - df['NormalCost']) / (df['NormalDuration'] - df['CrashDuration'])

    crash_plan = df.sort_values(by='CrashCostPerDay')
    crash_plan = crash_plan[['Activity', 'NormalDuration', 'CrashDuration', 'NormalCost', 'CrashCost', 'CrashCostPerDay']]
    return crash_plan
