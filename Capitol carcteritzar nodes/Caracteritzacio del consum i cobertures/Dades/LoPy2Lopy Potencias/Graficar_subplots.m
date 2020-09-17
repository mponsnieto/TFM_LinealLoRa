
filename = 'ProvaLopy2LopyPotencies';
sheet = 1;

dadesC1 = xlsread(filename,1);
dadesC2 = xlsread(filename,2);
t=dadesC1(:,1);
volt_C1=dadesC1(:,2);
volt_C2=dadesC2(:,2);
figure(); plot(t,volt_C1,t,volt_C2);
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Consum de la placa en prova de potencies')
legend('Consum Lopy','Pin P12')

y1=5-volt_C1;
y2=volt_C2;
time=t;

%dadesC1 = xlsread(filename,3);
%dadesC2 = xlsread(filename,4);
%time=dadesC1(:,1);
%volt_C1=dadesC1(:,2);
%volt_C2=dadesC2(:,2);
figure();
subplot(2,1,1);
plot(t,y1)
ylabel('Consum LoPy (A)');
xlabel('Temps (s)')
title('Consums durant la prova Lopy2Lopy')

subplot(2,1,2); 
plot(t,y2);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')


offset_t=0.5 %s
%% Potencia minima (2)
t_pot2=t(find(time>5.553-offset_t & time<5.668+offset_t));
y1_pot2=y1(find(time>5.553-offset_t & time<5.668+offset_t));
y2_pot2=y2(find(time>5.553-offset_t & time<5.668+offset_t));
figure();
subplot(2,1,1);
plot(t_pot2,y1_pot2);
title('Consums a potència mínima');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_pot2,y2_pot2);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')
%% Potencia 4
t_pot4=t(find(time>5.97-offset_t & time<6.08+offset_t));
y1_pot4=y1(find(time>5.97-offset_t & time<6.08+offset_t));
y2_pot4=y2(find(time>5.97-offset_t & time<6.08+offset_t));
figure();
subplot(2,1,1);
plot(t_pot4,y1_pot4);
title('Consums a potència de transmissió = 4');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_pot4,y2_pot4);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')

%% Ptencia 6
t_pot6=t(find(time>6.385-offset_t & time<6.49+offset_t));
y1_pot6=y1(find(time>6.385-offset_t & time<6.49+offset_t));
y2_pot6=y2(find(time>6.385-offset_t & time<6.49+offset_t));
figure();
subplot(2,1,1);
plot(t_pot6,y1_pot6);
title('Consums a potència de transmissió = 6');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_pot6,y2_pot6);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')
%% Potencia 8
t_pot8=t(find(time>6.81-offset_t & time<6.9+offset_t));
y1_pot8=y1(find(time>6.81-offset_t & time<6.9+offset_t));
y2_pot8=y2(find(time>6.81-offset_t & time<6.9+offset_t));
figure();
subplot(2,1,1);
plot(t_pot8,y1_pot8);
title('Consums a potència de transmissió = 8');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_pot8,y2_pot8);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')

%% Potencia 10
t_mcp=t(find(time>7.22-offset_t & time<7.33+offset_t));
y1_mcp=y1(find(time>7.22-offset_t & time<7.33+offset_t));
y2_mcp=y2(find(time>7.22-offset_t & time<7.33+offset_t));
figure();
subplot(2,1,1);
plot(t_mcp,y1_mcp);
title('Consums a potència de transmissió = 10');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_mcp,y2_mcp);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')

%% Potencia 12
t_bmp=t(find(time>7.633-offset_t & time<7.748+offset_t));
y1_bmp=y1(find(time>7.633-offset_t & time<7.748+offset_t));
y2_bmp=y2(find(time>7.633-offset_t & time<7.748+offset_t));
figure();
subplot(2,1,1);
plot(t_bmp,y1_bmp);
title('Consums a potència de transmissió = 12');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_bmp,y2_bmp);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')
%% Potencia 14
t_start=t(find(time>8.649-offset_t & time<8.764+offset_t));
y1_start=y1(find(time>8.649-offset_t & time<8.764+offset_t));
y2_start=y2(find(time>8.649-offset_t & time<8.764+offset_t));
figure();
subplot(2,1,1);
plot(t_start,y1_start);
title('Consums a potència de transmissió = 14');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_start,y2_start);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')
%% Totes les potencies
figure();plot(y1_pot2);
hold on
plot(y1_pot4);
plot(y1_pot6);
plot(y1_pot8);
plot(y1_mcp);
plot(y1_bmp);
plot(y1_start);
title('Consum del node enviant a diferents potències');
ylabel('Consum LoPy (A)')