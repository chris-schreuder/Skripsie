import os
from coding.feature_extraction import extract_features
from coding.dtw import getCost, splitSearch, getCosts


class Pet:

    def getMaxLen(self):
        train=self.train
        max_len=[1000,1000,1000,1000,1000]
        for seq, label in zip(self.data['features'],self.data['names']):
            if label == train[0] and seq.shape[0]<max_len[0]:
                max_len[0] = seq.shape[0]
            elif label == train[1] and seq.shape[0]<max_len[1]:
                max_len[1] = seq.shape[0]
            elif label == train[2] and seq.shape[0]<max_len[2]:
                max_len[2] = seq.shape[0]
            elif label == train[3] and seq.shape[0]<max_len[3]:
                max_len[3] = seq.shape[0]
            elif label == train[4] and seq.shape[0]<max_len[4]:
                max_len[4] = seq.shape[0]
        return max_len

    def loadData(self):
        seq = []
        clusters = []
        for folder in os.listdir('./audio'):
            if 'wav' not in folder:
                cluster = folder
                for file in os.listdir('./audio/' + folder):
                    os.remove('./audio/' + folder + '/' + file)
        data = {'features': seq, 'names': clusters}
        return data

    def __init__(self, name):
        self.name = name
        self.state = 0
        self.train_instructions = [
            'name',
            'eat',
            'fetch',
            'lay',
            'sit',
        ]
        self.train_count=[0,0,0,0,0]
        self.pet_imgs = [
            "img/pet_neutral.png",
            "img/pet_name.png",
            "img/pet_eating.png",
            "img/pet_fetch.png",
            "img/pet_laying.png",
            "img/pet_sitting.png",
        ]
        self.train=['eat', 'fetch', 'sit', 'name', 'lay']
        self.pet_img = self.pet_imgs[self.state]
        self.data = self.loadData()
        self.trainMaxLen = self.getMaxLen()
        self.command_seq = []
        self.command_name = ''

    def addTraining(self, name, filepath):
        signal_seq = extract_features(filepath)
        print('len: '+str(len(signal_seq)))
        if len(signal_seq) >= 10:
            seq = self.data['features']
            seq.append(signal_seq)
            names = self.data['names']
            names.append(name)
            self.data = {'features': seq, 'names': names}
            self.trainMaxLen = self.getMaxLen()
            print('training added')
        else:
            print('signal too short')

    
    # def interpretCommand(self):
    #     command_seq = extract_features('./audio/command.wav')
    #     min_cost = 10
    #     min_name = ''
    #     min_seq = []
    #     for seq, name in zip(self.data['features'], self.data['names']):
    #         print(seq.shape)
    #         path, cost_mat, cost_mat_normalized = getCost(command_seq, seq)
    #         cost= cost_mat_normalized[-1, -1].tolist()
    #         print(cost_mat_normalized[-1, -1].tolist())
    #         if cost < min_cost:
    #             min_cost = cost_mat_normalized[-1, -1].tolist()
    #             min_name = name
    #             min_seq = seq
    #     self.command_name = min_name
    #     self.command_seq = min_seq ##take out!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #     return min_cost, min_name

    def getComp(self, command_seq):
        step_size = 3
        seg_list=[[],[],[],[],[]]
        for item in self.train:
            for train_label, seq in zip(self.data['names'], self.data['features']):
                if item == train_label:
                    if self.train_count[self.train_instructions.index(item)] > 0:
                        if len(seg_list[self.train.index(item)]) == 0:
                            seq_len=self.trainMaxLen[self.train.index(item)]
                            segments_temp = splitSearch(seq_len, command_seq, step_size)
                            seg_list[self.train.index(item)] = segments_temp
        comp_label=[]
        comp_segments=[]
        comp_costs=[]
        for seq, name in zip(self.data['features'], self.data['names']):
            if self.train_count[self.train_instructions.index(name)] > 0:
                for item in self.train:
                    if item == name:
                        segments=seg_list[self.train.index(item)]
                costs = getCosts(seq, segments)
                comp_label.append(name)
                comp_segments.append(segments)
                comp_costs.append(costs)
        all_comp={'label': comp_label, 'seg': comp_segments, 'costs': comp_costs}
        return all_comp

    def getAvg(self, all_comp):
        avg_costs=[]
        avg_label=[]
        avg_segments=[]
        for item in self.train:
            if self.train_count[self.train_instructions.index(item)] > 0:
                costs_avg=[]
                count=0
                seg_temp=[]
                for train_label, costs, segments in zip(all_comp['label'], all_comp['costs'], all_comp['seg']):
                    if item == train_label:
                        seg_temp=segments
                        count+=1
                        if len(costs_avg) == 0:
                            costs_avg=[0]*len(costs)
                            for i in range(len(costs)):
                                costs_avg[i]=costs_avg[i]+costs[i]
                        else: 
                            for i in range(len(costs)):
                                costs_avg[i]=costs_avg[i]+costs[i]
                        print('avg2:'+ str(len(costs_avg)))
                for i in range(len(costs_avg)):
                    costs_avg[i]=costs_avg[i]/float(count)
                avg_label.append(item)
                avg_segments.append(seg_temp)
                avg_costs.append(costs_avg)
                print('****************cost2:'+ str(len(costs_avg)))
                print('******************seg:'+ str(len(seg_temp)))
        avg_comp={'label': avg_label, 'seg': avg_segments, 'costs': avg_costs}
        return avg_comp

    def interpretCommand(self):
        self.command_seq = []
        self.command_name = ''
        command_seq1 = extract_features('./audio/command.wav')
        min_cost = 10
        min_name = ''
        all_comp = self.getComp(command_seq1)
        avg_comp = self.getAvg(all_comp)
        for train_label, costs, seg in zip(avg_comp['label'], avg_comp['costs'], avg_comp['seg']):
            if self.train_count[self.train_instructions.index(train_label)] > 0:
                min_temp = min(costs)
                if min_temp < min_cost:
                    min_cost = min_temp
                    pred_temp = train_label
                    print("len cost: "+str(len(costs)))
                    print("len seg: "+str(len(seg)))
                    print("len index: "+str(costs.index(min_cost)))
                    pred_seg = seg[costs.index(min_cost)]
        if min_cost <= 0.006:
            self.command_name = pred_temp
            self.command_seq = pred_seg 
        else:
            pred_temp='None'
        return min_cost, pred_temp

    def savePraise(self):
        if self.command_name != '':
            print('len: '+str(self.command_seq.shape))
            if len(self.command_seq[0]) >= 10:
                seq = self.data['features']
                seq.append(self.command_seq)
                name = self.data['names']
                name.append(self.command_name)
                self.data = {'features': seq, 'names': name}
                self.command_seq = []
                self.command_name = ''
                print('praised')
            else:
                print('signal too short')

    def scoldPet(self):
        print('len: '+str(self.command_seq.shape))
        self.command_seq = []
        self.command_name = ''
        print('scolded')