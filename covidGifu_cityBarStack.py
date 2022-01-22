#
# �򕌌��V�^�R���i�E�C���X�����ǂɊւ��錧���̊��������A���������A���k��t����
# �s�����ʃO���t�쐬�@�ςݏグ�_�O���t
#
# partial release history:
# 2022/1/22 m.maruyama   Created
#
import csv, os
import glob
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
from datetime import date, timedelta

# �t�H���_����CSV�t�@�C���̈ꗗ���擾
files = sorted(glob.glob('csv/*.csv'))
# �t�@�C�������擾
file_number = len(files)
# CSV�t�@�C���̒��g��ǂݏo���āA���X�g�`���ɂ܂Ƃ߂�
csv_list = []
for file in files:
    csv_list.append(pd.read_csv(file,encoding='shift_jis',skiprows=[1]))
# CSV�t�@�C���̌���
covid_data_org = pd.concat(csv_list)

#�s�v�ȗ���폜
covid_data_org.drop(
    covid_data_org.columns[[13, 14, 15, 16]], axis=1,inplace=True)

#�s�v�ȗ���폜
covid_data_org.drop([
    "�S���n�������c�̃R�[�h", 
    "�s���{����", 
    "�s�撬����", 
    "����_�N����", 
    "����_�N��", 
    "����_����", 
    "����_����", 
    "����_���", 
    "����_�Ǐ�", 
    "����_�n�q���̗L���t���O"], axis=1,inplace=True)

# ���\_�N�����@1�`10000�� "yyyy/m/d"�@10001���` "yyyy-mm-dd"
# ���t�����𓝈�
#covid_data_org.replace({'���\_�N����': {'-0': '/'}}, inplace=True)
#covid_data_org.replace({'���\_�N����': {'-': '/'}}, inplace=True)

#�s�������Ɋ����Ґ����W�v
covid_data = covid_data_org.groupby(['���\_�N����', '����_���Z�n'], as_index=False).count()

# _DEBUG
# �o��
#covid_data.to_csv('covid_data_out.csv')

# �O���t�pdf�쐬
# 42�s�������ɐݒ�
columns1 =[	"�򕌎s",
            "�H���s",
            "�e�����s",
            "�R���s",
            "����s",
            "�{���s",
            "�}����",
            "��쒬",
            "�k����",
            "��_�s",
            "�C�Îs",
            "�{�V��",
            "�փP����",
            "���䒬",
            "������",
            "�_�˒�",
            "�֔V����",
            "�r�c��",
            "�K��쒬",
            "��쒬",
            "�֎s",
            "���Z�s",
            "���Z���Ύs",
            "���s",
            "�S��s",
            "��Ӓ�",
            "��j��",
            "���쒬",
            "�x����",
            "�����쑺",
            "���@��",
            "���S�Ò�",
            "�䐓��",
            "�������s",
            "���Ð�s",
            "���Q�s",
            "�b�ߎs",
            "�y��s",
            "���R�s",
            "��ˎs",
            "���C�s",
            "���쑺"]

# 42�s�����ʃJ���[
colorlist =["#aaaaff",
            "#8080ff",
            "#5555ff",
            "#2b2bff",
            "#0000ff",
            "#0000d5",
            "#0000aa",
            "#0000aa",
            "#000080",
            "#ffaaaa",
            "#ff8080",
            "#ff5555",
            "#ff2b2b",
            "#ff2b2b",
            "#ff0000",
            "#ff0000",
            "#ff0000",
            "#d50000",
            "#d50000",
            "#d50000",
            "#aaffaa",
            "#80ff80",
            "#55ff55",
            "#2bff2b",
            "#00ff00",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00aa00",
            "#ffaad5",
            "#ff80bf",
            "#ff55aa",
            "#ff2b95",
            "#ff0080",
            "#aad5ff",
            "#80bfff",
            "#55aaff",
            "#2b95ff"]

# X���f�[�^���X�g
# �w������獡���܂ł̍s��ݒ�
#d1 = date(2020,2,26)
d1 = date(2022,1,1)
d2 = datetime.date.today()

xDate = []
for i in range((d2 - d1).days + 1):
    date = d1 + timedelta(i)
    xDate.append(date)
    
# Y���f�[�^�񎟌��z��
yData = []

# 42�s�����{���t�������ɊY���s�𒊏o
for col, city in enumerate(columns1):
    covid_df1 = covid_data[covid_data['����_���Z�n'] == city]
    yDataCity = []

    # ���t�������ɊY���s�𒊏o
    for row, date1 in enumerate(xDate):
        strdate = date1.strftime('%Y-%m-%d')
#        strdate = strdate.replace('/0', '/')
        covid_df2 = covid_df1[covid_df1['���\_�N����'] == strdate]
        if len(covid_df2) :
            yDataCity.append(covid_df2.iat[0, 2])
        else :
            yDataCity.append(0)
    # Y���f�[�^�Ɏs�����ʃf�[�^��ǉ�
    yData.append(yDataCity)
'''
# _DEBUG
# �e�L�X�g�o��
with open('GraphData.txt', 'w') as f:
    f.write('\t')
    for item in xDate:
        f.write(item.strftime('%Y/%m/%d\t'))
    f.write('\n')

    for num, iCity in enumerate(yData):
        f.write(columns1[num] + '\t')
        for i in iCity:
            f.write(str(i) + '\t')
        f.write('\n')
'''
# �O���t�T�C�Y
fig, ax = plt.subplots(figsize=(12, 6))

# �ςݏグ�_�O���t�Ƀf�[�^���Z�b�g
# �s���������A�ςݏグ���J��Ԃ�
for i in range(len(yData)):
    if i != 0:
        ax.bar(xDate, yData[i], bottom=yData[i-1], color = colorlist[i])
    else:
        ax.bar(xDate, yData[i], color = colorlist[i])

# �^�C�g��
dt_now = datetime.datetime.now()
plt.title("�򕌌����̊��������i�s�����ʁj" + dt_now.strftime('%Y-%m-%d %H:%M:%S') + " ����", fontname="MS Gothic")

# �����x��
plt.ylabel("�l��", fontname="MS Gothic")

# ���ڐ�
#plt.yticks(np.arange(0, 500, step=50))

# �}��
plt.legend(columns1,
        bbox_to_anchor=(1.05, 1), 
		loc='upper left', 
		borderaxespad=0, 
		fontsize=12, 
		ncol=3, 
		prop={"family":"MS Gothic"})

# �摜�t�@�C���ۑ�
strfname = 'png/' + d2.strftime('%Y%m%d') + '_covidGifu_cityBarStack.png'
plt.savefig(strfname, bbox_inches='tight')

plt.show()
plt.close('all')
