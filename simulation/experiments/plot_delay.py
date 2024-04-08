import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# plt.style.use('seaborn-poster')


# "load_info_staleness" or "placement_info_staleness" or "req_inter_arrival_delay"
INDEPENDENT_VARIABLE = "load_info_staleness"
scheduler_type = "decentralheft"

current_file_location = os.path.dirname(os.path.abspath(__file__))
log_data_path = os.path.join(current_file_location, "/results/stacked/" + scheduler_type + "/")
log_data_path = "./results/stacked/" + scheduler_type + "/"
print(log_data_path)
dataframe = pd.DataFrame(columns=["job_id", "load_info_staleness", "placement_info_staleness", "req_inter_arrival_delay",
                                  "workflow_type", "scheduler_type", "slowdown", "response_time"])

for file in os.listdir(log_data_path):
    if os.path.isfile(os.path.join(log_data_path, file)):
        current_dataframe = pd.read_csv(os.path.join(log_data_path, file))
        dataframe = pd.concat([dataframe, current_dataframe], ignore_index=True)
        # print(dataframe)


def make3Dplot(dataset):

    x = sorted(dataset["load_info_staleness"].dropna().unique())
    print(x)
    y = sorted(dataset["placement_info_staleness"].dropna().unique())
    print(y)

    Z = np.zeros((len(y), len(x)))
    Z_workflow0 = np.zeros((len(y), len(x)))
    Z_workflow1 = np.zeros((len(y), len(x)))
    Z_workflow2 = np.zeros((len(y), len(x)))
    Z_workflow3 = np.zeros((len(y), len(x)))

    X, Y = np.meshgrid(x, y)

    print("X: ", x)
    print("Y: ", y)

    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection='3d')
    ax.grid()

    for index_x, x in enumerate(x):

        df_x = dataframe.loc[dataframe["load_info_staleness"] == x]
        for index_y, y in enumerate(y):
            print("---", x, y)
            df_y = df_x.loc[dataframe["placement_info_staleness"] == y]

            df_workflow0 = df_y.loc[df_y["workflow_type"] == 0]
            df_workflow1 = df_y.loc[df_y["workflow_type"] == 1]
            df_workflow2 = df_y.loc[df_y["workflow_type"] == 2]
            df_workflow3 = df_y.loc[df_y["workflow_type"] == 3]

            Z[index_y, index_x] = np.average(df_y["response_time"])
            Z_workflow0[index_y, index_x] = np.average(df_workflow0["response_time"])
            Z_workflow1[index_y, index_x] = np.average(df_workflow1["response_time"])
            Z_workflow2[index_y, index_x] = np.average(df_workflow2["response_time"])
            Z_workflow3[index_y, index_x] = np.average(df_workflow3["response_time"])

        y = sorted(dataset["placement_info_staleness"].dropna().unique())

    #print("Z: ", Z)
    #ax.scatter3D(X, Y, Z, color='black')
    #ax.plot_surface(X,Y,Z)

    ax.plot_wireframe(X, Y, Z, color='black', alpha=0.8)

    #ax.plot_wireframe(X, Y, Z_workflow0, color='black')
    #ax.plot_wireframe(X, Y, Z_workflow1, color='blue')
    #ax.plot_wireframe(X, Y, Z_workflow2, color='orange')
    #ax.plot_wireframe(X, Y, Z_workflow3, color='red')
    #ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_title('End-to-end job latency. Creation interval: 5 ms.')

    # Set axes label
    ax.set_xlabel('load_info_staleness (ms)', labelpad=20)
    ax.set_ylabel('placement_info_staleness (ms)', labelpad=20)
    ax.set_zlabel('End-to-end job latency (ms)', labelpad=20)

    plt.show()


def plot_stacked_bars(dataframe):
    sns.set_style(style="white")
    #plt.figure(figsize=(12, 8))

    dataframe = dataframe.drop(["job_id", "load_info_staleness", "placement_info_staleness", "req_inter_arrival_delay", "scheduler_type", "slowdown", "response_time",
                                  "Unnamed: 0"], axis=1)
    
    JOB_TYPE = 3
    TASK_TYPE = 2
    SCHEDULER_NAME = "decentralheft"
    newdf = dataframe.loc[dataframe["workflow_type"] == JOB_TYPE]
    newdf = newdf.loc[newdf["task_id"] == TASK_TYPE]
    # newdf = newdf.loc[newdf["scheduler_name"] == TASK_TYPE]
    newdf = newdf.drop(["workflow_type", "task_id"], axis=1)

    # Print only the first 100 rows
    newdf.drop(newdf.index[:-200], axis=0, inplace=True)

    # create stacked bar chart
    newdf.plot(kind='bar', stacked=True)

    # add overall title
    plt.title(f'Breakdown of the end-to-end delay. Workflow: {JOB_TYPE}. Task_type {TASK_TYPE}.', fontsize=16)

    # add axis titles
    plt.xlabel('')
    plt.ylabel('Delay (ms)')

    plt.xticks([], [])

    plt.show()


def plot_aggregated_stacked_bars(dataframe):
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(12, 8))

    dataframe = dataframe.drop(["job_id", "load_info_staleness", "placement_info_staleness", "req_inter_arrival_delay", "scheduler_type", "slowdown", "response_time",
                                   "Unnamed: 0"], axis=1)

    JOB_TYPE = 2
    # centralheft|decentralheft|hashtask
    SCHEDULER_NAME = "hashtask"

    df_selected_sched = dataframe.loc[dataframe["scheduler_name"] == SCHEDULER_NAME]
    df_selected_job = df_selected_sched.loc[df_selected_sched["workflow_type"] == JOB_TYPE]
    df_selected_job = df_selected_job.drop(["workflow_type"], axis=1)

    # Drop the first 500
    df_selected_job.drop(df_selected_job.index[:500], axis=0, inplace=True)
    #print(df_selected_job.to_string())

    #final_dataframe = pd.DataFrame(columns=["scheduler_name",  "task_id", "time_to_buffer", "dependency_wait_time", "time_spent_in_queue", "model_fetching_time", "execution_time"])

    dff = df_selected_job.groupby("task_id")[["time_to_buffer", "dependency_wait_time", "time_spent_in_queue", "model_fetching_time", "execution_time"]].mean().reset_index()
    dff_std = df_selected_job.groupby("task_id")[["time_to_buffer", "dependency_wait_time", "time_spent_in_queue", "model_fetching_time", "execution_time"]].std().reset_index()

    dff["task_id"] = dff["task_id"].astype(int)
    dff_std["task_id"] = dff_std["task_id"].astype(int)
    print(dff.to_string())

    # create stacked bar chart![](figures/stacked_decentralheft_workflow1.png)
#    plt.subplot(211)
    dff.plot(x="task_id", yerr=dff_std, kind="bar", stacked=True)



    # add overall title
    plt.title(f'End-to-end latency breakdown. Scheduler: {SCHEDULER_NAME}. Workflow: {JOB_TYPE}.', fontsize=20)

    # add axis titles
    plt.xlabel('Task type')
    plt.ylabel('Delay (ms)')

    #plt.xticks([], [])
    plt.xticks(rotation=0)  # Rotates X-Axis Ticks by 45-degrees
    plt.ylim(0, 300)

    plt.show()



def plot_mean_std(df, title_name):
    fig, ax = plt.subplots()
    plt.figure(figsize=(16, 8))
    for key, group in df.groupby('type'):
        group.plot('load_info_staleness', 'slowdown_mean',
                   yerr='slowdown_std', label=key, ax=ax)
        # group.plot('info delay', 'slowdown_mean', label=key, ax=ax)
    plt.ylabel("End-to-end Responde Time(ms)", fontsize=14)
    plt.xlabel("Information Delay(ms)", fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title(title_name, fontsize=15)
    plt.show()


def plot_delay_with_seaborn(dataframe, title_name):
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # ax = sns.lineplot(data=dataframe)
    sns.lineplot(x=INDEPENDENT_VARIABLE, y="response_time",
                 hue="workflow_type", style="scheduler_type", markers=True, err_style="bars", data=dataframe)
    # ax.set_yscale("log")
    plt.ylabel("Execution time (ms)", fontsize=20)
    plt.xlabel(INDEPENDENT_VARIABLE + " (ms)", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(title_name, fontsize=20)

    plt.show()


def scatter_plot_across_workflows(dataframe, title_name):
    sns.set_style(style="whitegrid")

    sns.scatterplot(x="job_id", y="response_time",
                    hue="workflow_type", data=dataframe)
    # ax.set_yscale("log")
    plt.ylabel("End-to-end execution time (ms)", fontsize=20)
    plt.xlabel("job_id", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(title_name, fontsize=20)

    plt.show()


def scatter_plot_across_schedulers(dataframe, title_name):
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # ax = sns.lineplot(data=dataframe)
    newdf = dataframe.loc[dataframe["workflow_type"] == 3]
    sns.scatterplot(x="job_id", y="response_time",
                    hue="scheduler_type", s=24, data=newdf)
    # ax.set_yscale("log")
    plt.ylabel("End-to-end execution time (ms)", fontsize=20)
    plt.xlabel("job_id", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(title_name, fontsize=20)

    plt.show()






# plot_delay_with_seaborn(dataframe, "Total execution delay")

#scatter_plot_across_schedulers(dataframe,  "Execution time for Workflow 3")
# make3Dplot(dataset=dataframe)
plot_stacked_bars(dataframe)
#plot_aggregated_stacked_bars(dataframe)
#scatter_plot_across_workflows(dataframe, "HEFT-based scheduling")
