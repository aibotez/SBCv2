%%
clear all;
shotnumber=220110012
mdsconnect('10.62.0.2')
mdsopen('ncst',shotnumber)
%80Channels:����Ȧ��I_RC,14������IP��I_Plasma,3��������ͨ����FLUX_Fay,10������ ����ѹ��FLUX_Vloop,10����
%����̽�루FBIpol,16�����������׶�ŵ��̽�루Mpol,16�����������׶�ŵ��̽�루Npol��10����.
%%
% %ƽ������
% smooth_span=0.002;
% smooth_method='loess';
%%
ReflI     =  mdsvalue('rawdata:acq2106_198:site1:input_01'); 
ReflQ     =  mdsvalue('rawdata:acq2106_198:site1:input_02');
ReflWave  =  mdsvalue('rawdata:acq2106_198:site1:input_03'); 
time_NCST = mdsvalue('dim_of(rawdata:acq2106_196:site4:input_01)');

% fs = 20*10^6;
% time = 1/fs:1/fs:0.2;