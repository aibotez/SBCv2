%%
clear all;
shotnumber=220110012
mdsconnect('10.62.0.2')
mdsopen('ncst',shotnumber)
%80Channels:场线圈（I_RC,14道）、IP（I_Plasma,3道）、磁通环（FLUX_Fay,10道）、 环电压（FLUX_Vloop,10道）
%、磁探针（FBIpol,16道）、极向米尔诺夫探针（Mpol,16道）、环向米尔诺夫探针（Npol，10道）.
%%
% %平滑处理
% smooth_span=0.002;
% smooth_method='loess';
%%
ReflI     =  mdsvalue('rawdata:acq2106_198:site1:input_01'); 
ReflQ     =  mdsvalue('rawdata:acq2106_198:site1:input_02');
ReflWave  =  mdsvalue('rawdata:acq2106_198:site1:input_03'); 
time_NCST = mdsvalue('dim_of(rawdata:acq2106_196:site4:input_01)');

% fs = 20*10^6;
% time = 1/fs:1/fs:0.2;