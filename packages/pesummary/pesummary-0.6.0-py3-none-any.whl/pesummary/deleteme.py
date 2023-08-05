from pesummary.utils.samples_dict import MCMCSamplesDict
parameters = ["A", "b"]
samples = [[[1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6], [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]], [[0.8, 0.5, 1.7, 1.4, 1.2, 1.7, 0.9], [10, 10.5, 10.4, 9.6, 8.6, 11.6, 16.2]]]
dataset = MCMCSamplesDict(parameters, samples)
print(dataset)
print(dataset.gelman_rubin("b"))
g = dataset.T
print(g)
print(g.gelman_rubin("b"))
