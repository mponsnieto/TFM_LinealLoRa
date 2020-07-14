%root='C:\Users\Vicenç Salas\Desktop\CAP1\Lab Tomeu 26_11';
%% Prova deixant el gateway al despatx de'n Tomeu 100msg 10 minuts
%  comparació del nombre de missatje rebut i enviat

filename = 'Datos 26_11';
sheet = 1;

dadesNRed = xlsread(filename,1);
dadesLoPy = xlsread(filename,2);
counterNR=dadesNRed(:,1);
counterLoPy=dadesLoPy(:,2);
%%
PSRR=length(counterNR)/length(counterLoPy)*100; % PSRR=98.61%
aux=[1];
j=2;%ttn console
k=2;
for (i=2:1:length(counterLoPy)-1)
    if j<length(counterNR)
        cNR=counterNR(j);
    else
        cNR=0;
    end
    if cNR/counterLoPy(i)==1
        aux=[aux 1];
        j=j+1;
    else
        aux =[aux 0];
    end
    
end
figure();
plot(1:1:length(counterLoPy)-1,aux);
ylim([-0.5,1.5]);
title('Missatges rebuts (o perduts)');
xlabel('Nombre de missatge');
ylabel('Rebut = 1, Perdut = 0');





