import os

from torch.utils.data import Dataset
class my_dataset(Dataset):
    def __init__(self,root_dir):
        super(my_dataset,self).__init__()
        self.image_path=[os.path.join(root_dir,image_name) for image_name in os.listdir(root_dir)]
        print(self.image_path)

    def __len__(self):
        return self.image_path.__len__()

    def __getitem__(self, index):
        image_path = self.image_path[index]
        print(image_path)

if __name__ == '__main__':
    train_data = my_dataset("../test_data")
    train_data[1]