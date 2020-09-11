%% Place this file in the repo of Baph2.0 - Matlab in the folder braph2 to be able to run it

%% Test single measure

clear all
clc

directory = fileparts(which('braph2'));

addpath(directory)
addpath([directory filesep 'util'])
addpath([directory filesep 'graph'])
addpath([directory filesep 'graph' filesep 'graphs'])
addpath([directory filesep 'graph' filesep 'measures'])

A = [0, 0.1, 0.2, 0.1, 0, 0, 0, 0
     0, 0, 0.5, 0, 0.1, 0, 0, 0
     0, 0, 0, 0, 0.2, 0, 0, 0
     0, 0, 0.5, 0, 0.1, 0, 0, 0
     0, 0, 0.2, 0, 0, 0.1, 0.5, 0
     0, 0, 0, 0, 0, 0, 0, 0.2
     0, 0, 0, 0, 0, 0, 0, 0.8
     0, 0, 0, 0, 0, 0, 0, 0];
 
graph = GraphBU(A);
measure = LocalEfficiency(graph);
le = measure.getValue()

%% Test all measures

clear all
clc

directory = fileparts(which('braph2'));

addpath(directory)
addpath([directory filesep 'util'])
addpath([directory filesep 'graph'])
addpath([directory filesep 'graph' filesep 'graphs'])
addpath([directory filesep 'graph' filesep 'measures'])

matrices = load('matlab_matrix.mat');
graph_types = {'GraphBU', 'GraphBD', 'GraphWU', 'GraphWD'};
for i = 1:length(fieldnames(matrices)) % for all matrices
    disp(i)
    matrix_name = strcat('matrix_', int2str(i));
    matrix = matrices.(matrix_name);
    for j = 1:length(graph_types) % for all graph types
        graph_type = graph_types{j};
        graph = eval(strcat(graph_type, '(matrix)'));
        measures = Graph.getCompatibleMeasureList(graph);
        for k = 1:length(measures) % for all compatible measures
            measure = measures{k};
            if strncmp('RichClub', measure, 8) % not implemented in python
                continue;
            end
            m = eval(strcat(measure, '(graph)'));
            value = m.getValue();
            output.(matrix_name).(graph_type).(measure) = value;
        end
    end
end

save('matlab_output.mat', 'output')

%% test bu
A = [0, 1, 0, 1, 0, 0, 0, 0
     0, 0, 1, 0, 1, 0, 0, 0
     1, 0, 0, 0, 1, 0, 0, 0
     0, 0, 1, 0, 1, 0, 0, 0
     0, 0, 0, 0, 0, 1, 1, 0
     0, 0, 0, 0, 0, 0, 0, 1
     0, 0, 0, 0, 0, 0, 0, 1
     0, 0, 0, 0, 0, 0, 0, 0];
 
graph = GraphBU(A);
measure = LocalEfficiency(graph);
le = measure.getValue()

%% test wu

A = [0, 0.1, 0.2, 0.1, 0, 0, 0, 0
     0, 0, 0.5, 0, 0.1, 0, 0, 0
     0, 0, 0, 0, 0.2, 0, 0, 0
     0, 0, 0.5, 0, 0.1, 0, 0, 0
     0, 0, 0.2, 0, 0, 0.1, 0.5, 0
     0, 0, 0, 0, 0, 0, 0, 0.2
     0, 0, 0, 0, 0, 0, 0, 0.8
     0, 0, 0, 0, 0, 0, 0, 0];
 
graph = GraphWU(A);
measure = LocalEfficiency(graph);
le = measure.getValue()
 