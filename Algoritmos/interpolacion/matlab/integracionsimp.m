function [I, x] = simpson_1_3_compuesto(f, a, b, n)
% SIMPSON_1_3_COMPUESTO Regla de Simpson 1/3 compuesto
%
% Sintaxis: [I, x] = simpson_1_3_compuesto(f, a, b, n)
%
% Parámetros:
%   f - Handle de la función
%   a, b - Límites de integración
%   n - Número de subintervalos (DEBE SER PAR)
%
% Retorna:
%   I - Aproximación de la integral
%   x - Puntos de evaluación

    % Verificar que n sea par
    if mod(n, 2) ~= 0
        error('n debe ser par para Simpson 1/3');
    end
    
    % Generar puntos
    x = linspace(a, b, n+1);
    h = (b - a) / n;
    
    % Evaluar función
    y = f(x);
    
    % Fórmula de Simpson 1/3
    % Pesos: 1, 4, 2, 4, 2, ..., 4, 1
    I = y(1) + y(end);
    
    % Índices impares: peso 4
    I = I + 4 * sum(y(2:2:end-1));
    
    % Índices pares (internos): peso 2
    I = I + 2 * sum(y(3:2:end-2));
    
    I = I * h / 3;
end


function I = simpson_1_3_simple(f, a, b)
% SIMPSON_1_3_SIMPLE Regla de Simpson 1/3 simple
    h = (b - a) / 2;
    c = (a + b) / 2;
    I = (h / 3) * (f(a) + 4*f(c) + f(b));
end


% ========================================================================
% SCRIPT DE EJEMPLO
% ========================================================================

fprintf('========================================\n');
fprintf('REGLA DE SIMPSON 1/3 COMPUESTO\n');
fprintf('========================================\n\n');

% Ejemplo 1: ∫[0,1] x² dx = 1/3
fprintf('EJEMPLO 1: ∫[0,1] x² dx\n');
fprintf('----------------------------------------\n\n');

f1 = @(x) x.^2;
a = 0;
b = 1;
I_real = 1/3;

fprintf('Valor real: %.10f\n\n', I_real);
fprintf('%-10s %-20s %-15s %-15s\n', 'n', 'Aproximación', 'Error', 'Error Rel. (%)');
fprintf('----------------------------------------------------------------\n');

ns = [2, 4, 8, 16, 32];
for i = 1:length(ns)
    n = ns(i);
    [I, ~] = simpson_1_3_compuesto(f1, a, b, n);
    error = abs(I - I_real);
    error_rel = error / abs(I_real) * 100;
    fprintf('%-10d %-20.10f %-15.2e %-15.6f\n', n, I, error, error_rel);
end

% Ejemplo 2: ∫[0,1] e^x dx = e - 1
fprintf('\n\n');
fprintf('EJEMPLO 2: ∫[0,1] e^x dx = e - 1\n');
fprintf('----------------------------------------\n\n');

f2 = @(x) exp(x);
I_real2 = exp(1) - 1;
n = 10;

[I, x] = simpson_1_3_compuesto(f2, 0, 1, n);
error = abs(I - I_real2);

fprintf('Número de subintervalos: %d\n', n);
fprintf('Aproximación: %.10f\n', I);
fprintf('Valor real:   %.10f\n', I_real2);
fprintf('Error:        %.2e\n', error);

% Comparar métodos
comparar_trapecio_simpson(f2, 0, 1, I_real2);


function comparar_trapecio_simpson(f, a, b, I_real)
% Compara Trapecio vs Simpson
    
    fprintf('\n\n');
    fprintf('========================================\n');
    fprintf('COMPARACIÓN: TRAPECIO vs SIMPSON 1/3\n');
    fprintf('========================================\n\n');
    
    fprintf('%-10s %-20s %-15s %-20s %-15s\n', ...
            'n', 'Trapecio', 'Error Trap.', 'Simpson', 'Error Simp.');
    fprintf('--------------------------------------------------------------------------------\n');
    
    ns = [2, 4, 8, 16, 32];
    errores_trap = zeros(size(ns));
    errores_simp = zeros(size(ns));
    
    for i = 1:length(ns)
        n = ns(i);
        
        % Trapecio
        [I_trap, ~] = trapecio_compuesto(f, a, b, n);
        error_trap = abs(I_trap - I_real);
        
        % Simpson
        [I_simp, ~] = simpson_1_3_compuesto(f, a, b, n);
        error_simp = abs(I_simp - I_real);
        
        errores_trap(i) = error_trap;
        errores_simp(i) = error_simp;
        
        fprintf('%-10d %-20.10f %-15.2e %-20.10f %-15.2e\n', ...
                n, I_trap, error_trap, I_simp, error_simp);
    end
    
    % Graficar
    figure('Position', [100, 100, 800, 600]);
    loglog(ns, errores_trap, 'ro-', 'LineWidth', 2, 'MarkerSize', 8); hold on;
    loglog(ns, errores_simp, 'bs-', 'LineWidth', 2, 'MarkerSize', 8);
    grid on;
    xlabel('Número de subintervalos (n)', 'FontSize', 12);
    ylabel('Error absoluto', 'FontSize', 12);
    title('Convergencia: Trapecio vs Simpson', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Trapecio', 'Simpson 1/3', 'FontSize', 12);
    
    fprintf('\n✅ Gráfica generada\n');
end