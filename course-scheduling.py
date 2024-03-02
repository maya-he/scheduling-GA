import numpy as np 
import copy 

class Schedule:
    def __init__(self,courseID,classID,profID):
        self.courseID = courseID
        self.classID = classID
        self.profID = profID
        
        self.roomID = 0 
        self.weekDAY = 0 
        self.slot = 0
        
    def randominit(self,roomrange):
        #room range : int,number of classrooms
        self.roomID = np.random.randint(1,roomrange+1,1)[0]
        self.weekDAY = np.random.randint(1, 6, 1)[0]
        self.slot = np.random.randint(1, 6, 1)[0]
        
#calculate the conflicts 
def schedule_cost(population,best):
    #population : list of class schedules
    #best : number of best results 
    conflicts = [] 
    n = len(population[0])
    for p in population:
        conflict = 0 
        for i in range(0, n-1):
            for j in range(i+1,n):
                #in the same time and the same room
                if p[i].roomID == p[j].roomID and p[i].weekDAY == p[j].weekDAY and p[i].slot == p[i].slot:
                    conflict +=1  
                #for one professor at the same time 
                if p[i].profID == p[j].profID and p[i].weekDAY == p[j].weekDAY and p[i].slot == p[j].slot:
                    conflict += 1
                # check course for one class in same time
                if p[i].classID == p[j].classID and p[i].weekDAY == p[j].weekDAY and p[i].slot == p[j].slot:
                    conflict += 1
                # check same course for one class in same day
                if p[i].classID == p[j].classID and p[i].courseID == p[j].courseID and p[i].weekDAY == p[j].weekDAY:
                    conflict += 1
        conflicts.append(conflict)
    idx = np.array(conflicts).argsort()
    #return : index of best result , best conflict score
    return idx[:best], conflicts[idx[0]]

class genetic:
    def __init__(self,popsize=20,mutprob=0.3,best=5,maxit=20):
        self.popsize = popsize
        self.mutprob = mutprob
        self.best = best
        self.maxit = maxit  # iteration times
        
    def population(self,schedules,roomrange):
        self.population = []
        for i in range(self.popsize):
            entity = []
            for s in schedules:
                s.randominit(roomrange)
                entity.append(copy.deepcopy(s))
            self.population.append(entity)
    
    def mutation(self,bestpopulation,roomrange):
        #bestpopulation : best schedules
        b = np.random.randint(0,self.best,1)[0] #choosing randomly from the best parents
        #choose random position of a gene to be changed 
        pos = np.random.randint(0,2,1)[0]
        am = copy.deepcopy(bestpopulation[b]) #am = after mutation
        for p in am:
            pos = np.random.randint(0,3,1)[0]
            operation = np.random.rand()
            if pos == 0:
                p.roomID = self.addsub(p.roomID,operation,roomrange)
            if pos ==1:
                p.weekDAY = self.addsub(p.weekDAY,operation,5)
            if pos ==2:
                p.slot = self.addsub(p.slot,operation,5)
        return am
                
    #add or sub opertaion in mutation
    def addsub(self,value,op,valuerange):
        #value : value to be mutated
        #op : prob of operation 
        if op > 0.5:
            if value < valuerange:
                value +=1
            else:
                value -=1
        else:
            if value -1 > 0:
                value -=1
            else:
                value +=1
        #return mutated value
        return value
    
    def crossover(self,bestpopulation):
        #crossover between 2 random parents
        b1 = np.random.randint(0,self.best,1)[0] 
        b2 = np.random.randint(0,self.best,1)[0] 
        #random gene position
        pos = np.random.randint(0,2,1)[0] 
        ac1 = copy.deepcopy(bestpopulation[b1]) #ac = after crossover
        ac2 = bestpopulation[b2]
        for p1,p2 in zip(ac1,ac2):
            if pos == 0:
                p1.weekDAY = p2.weekDAY
                p1.slot = p2.slot
            if pos ==1:
                p1.roomID = p2.roomID 
        return ac1 
    
    def evolution(self,schedules,roomrange):
        #return index of best result , best conflict score 
        bestScore = 0 
        bestSchedule = None
        self.population(schedules,roomrange)
        for i in range(self.maxit):
            bestidx, bestScore = schedule_cost(self.population,self.best)
            print('Iter: {} | conflict: {}'.format(i + 1, bestScore))
            if bestScore == 0:
                bestSchedule = self.population[bestidx[0]]
                break
            newpop = [self.population[idx]for idx in bestidx]
            while len(newpop) < self.popsize:
                if np.random.rand() < self.mutprob:
                    # Mutation
                    newp = self.mutation(newpop, roomrange)
                else:
                    # Crossover
                    newp = self.crossover(newpop)
                newpop.append(newp)
            self.population = newpop
        return bestSchedule
    

schedules = []
# add schedule
#Schedule(course,class,prof)
schedules.append(Schedule('IS', 'CLASSA', 'Dr Ahmed'))
schedules.append(Schedule('IS', 'CLASSC', 'Dr Ahmed'))
schedules.append(Schedule('AI', 'CLASSA', 'Dr Ali'))
schedules.append(Schedule('AI', 'CLASSA', 'Dr Ali'))
schedules.append(Schedule('CS', 'CLASSC', 'Dr Sara'))
schedules.append(Schedule('CS', 'CLASSA', 'Dr Sara'))
schedules.append(Schedule('IT', 'CLASSA', 'Prof Mai'))
schedules.append(Schedule('IT', 'CLASSC', 'Prof Mai'))

schedules.append(Schedule('AI', 'CLASSB', 'Dr Ali'))
schedules.append(Schedule('AI', 'CLASSB', 'Dr Ali'))
schedules.append(Schedule('SE', 'CLASSC', 'Dr M'))
schedules.append(Schedule('SE', 'CLASSB', 'Dr M'))
schedules.append(Schedule('IT', 'CLASSB', 'Prof Mai'))
schedules.append(Schedule('IT', 'CLASSC', 'Prof Mai'))

ga = genetic(popsize=20, best=5, maxit=200)
res = ga.evolution(schedules, 3)
