import numpy as np
import pandas as pd

def load_offspring(df, fn):
    df_offspring = pd.read_json(fn)
    df_offspring.rename(columns={'child_id': 'Ind_ID'}, inplace=True)
    df_offspring.set_index(['Exp_Num', 'Ind_ID'], inplace=True)
    tallies = []
    for experiment_number in df.index.levels[0]:
        try:
            offspring_experiment = df_offspring.loc[experiment_number]
        except KeyError as e:
            continue

        vc1 = offspring_experiment.parent1_id.value_counts()
        vc2 = offspring_experiment.parent2_id.value_counts()
        tally = vc1.add(vc2, fill_value=0)
        tally = tally.to_frame()
        tally.columns = ['numberOfChildren']
        tally['Exp_Num'] = experiment_number
        tally.index = tally.index.rename('Ind_ID')
        tally.set_index(['Exp_Num', tally.index], inplace=True)
        tallies += [tally]
    df = df.join(pd.concat(tallies))
    return df

def load_meeting(df, fn):
    df_meeting = pd.read_json(fn)
    df_meeting.rename(columns={'indiv_id': 'Ind_ID'}, inplace=True)
    df_meeting.set_index(['Exp_Num', 'Ind_ID'], inplace=True)

    tallies = []
    for experiment_number in df.index.levels[0]:
        try:
            meeting_experiment = df_meeting.loc[experiment_number]
        except KeyError as e:
            continue
        meeting_experiment.reset_index(inplace=True)
        vc1 = meeting_experiment.Ind_ID.value_counts()
        vc2 = meeting_experiment.mate_indiv_id.value_counts()
        tally = vc1.add(vc2, fill_value=0)
        tally = tally.to_frame()
        tally.columns = ['numberOfMeeting']
        tally['Exp_Num'] = experiment_number
        tally.index = tally.index.rename('Ind_ID')
        tally.set_index(['Exp_Num', tally.index], inplace=True)
        tallies += [tally]
    df = df.join(pd.concat(tallies))
    return df
