function [I, R] = romberg(f, a, b, n_max, tol, mostrar_tabla)
% ROMBERG Método de Romberg para integración numérica
%
% Sintaxis: [I, R] = romberg(f, a, b, n_max, tol, mostrar_tabla)
%
% Parámetros:
%   f - Handle de la función a integrar
%   a, b - Límites de integración
%   n_max - Número máximo de niveles (opcional, default: 10)
%   tol - Tolerancia (opcional, default: 1e-8)
%   mostrar_tabla - Mostrar tabla (opcional, default: true)
%
% Retorna:
%   I - Aproximación de la integral
%   R - Tabla de Romberg

    % Valores por defecto
    if nargin < 4, n_max = 10; end
    if nargin < 5, tol = 1e-8; end
    if nargin < 6, mostrar_tabla = true; end

    % Inicializar tabla
    R = zeros(n_max, n_max);

    fprintf('========================================\n');
    fprintf('MÉTODO DE ROMBERG\n');
    fprintf('========================================\n\n');
    fprintf('Integrando en [%.4f, %.4f]\n', a, b);
    fprintf('Tolerancia: %.2e\n\n', tol);

    % Primera columna: Trapecio con n=1,2,4,8,...
    h = b - a;
    R(1, 1) = h * (f(a) + f(b)) / 2;

    % Construir tabla
    for i = 2:n_max
        % Calcular R(i,1) usando fórmula recursiva
        h = h / 2;
        suma = 0;

        % Sumar puntos intermedios
        for k = 1:2:(2^(i-1)-1)
            x_k = a + k * h;
            suma = suma + f(x_k);
        end

        R(i, 1) = R(i-1, 1) / 2 + h * suma;

        % Extrapolación de Richardson
        for j = 2:i
            R(i, j) = R(i, j-1) + (R(i, j-1) - R(i-1, j-1)) / (4^(j-1) - 1);
        end

        % Criterio de convergencia
        if i > 1 && abs(R(i, i) - R(i-1, i-1)) < tol
            fprintf('✅ Convergencia alcanzada en nivel %d\n', i-1);
            if mostrar_tabla
                mostrar_tabla_romberg(R, i);
            end
            I = R(i, i);
            R = R(1:i, 1:i);
            return;
        end
    end

    fprintf('⚠️  Se alcanzó el máximo de niveles (%d)\n', n_max);
    if mostrar_tabla
        mostrar_tabla_romberg(R, n_max);
    end

    I = R(n_max, n_max);
end


function mostrar_tabla_romberg(R, n_filas)
% Muestra la tabla de Romberg

    fprintf('\n');
    fprintf('========================================\n');
    fprintf('TABLA DE ROMBERG\n');
    fprintf('========================================\n\n');

    % Encabezado
    fprintf('%-5s', 'i');
    for j = 1:n_filas
        fprintf('%-20s', sprintf('R(i,%d)', j-1));
    end
    fprintf('\n');
    fprintf(repmat('-', 1, 80));
    fprintf('\n');

    % Datos
    for i = 1:n_filas
        fprintf('%-5d', i-1);
        for j = 1:i
            fprintf('%-20.12f', R(i, j));
        end
        fprintf('\n');
    end

    fprintf('========================================\n\n');

    % Análisis de convergencia
    fprintf('📊 Análisis de convergencia:\n');
    fprintf('%-10s %-20s %-20s\n', 'Nivel', 'R(i,i)', 'Error estimado');
    fprintf(repmat('-', 1, 50));
    fprintf('\n');

    for i = 1:min(n_filas, 8)
        if i == 1
            fprintf('%-10d %-20.12f %-20s\n', i-1, R(i,i), 'N/A');
        else
            error_est = abs(R(i,i) - R(i-1,i-1));
            fprintf('%-10d %-20.12f %-20.2e\n', i-1, R(i,i), error_est);
        end
    end
end


% ========================================================================
% SCRIPT DE EJEMPLO
% ========================================================================

fprintf('\n\n');
fprintf('🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍\n');
fprintf('EJEMPLO COMPLETO: ∫[0,1] x² dx = 1/3\n');
fprintf('🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍\n\n');

% Función
f1 = @(x) x.^2;
a = 0;
b = 1;
I_real = 1/3;

% Aplicar Romberg
[I, R] = romberg(f1, a, b, 6, 1e-10, true);

fprintf('\n✅ RESULTADO FINAL: %.15f\n', I);
fprintf('   Valor real:      %.15f\n', I_real);
fprintf('   Error absoluto:  %.2e\n', abs(I - I_real));

% Ejemplo 2: sin(x)
fprintf('\n\n');
fprintf('═══════════════════════════════════════\n');
fprintf('EJEMPLO 2: ∫[0,π] sin(x) dx = 2\n');
fprintf('═══════════════════════════════════════\n\n');

f2 = @(x) sin(x);
I_real2 = 2.0;

[I2, R2] = romberg(f2, 0, pi, 8, 1e-12, true);

fprintf('\n✅ RESULTADO FINAL: %.15f\n', I2);
fprintf('   Valor real:      %.15f\n', I_real2);
fprintf('   Error absoluto:  %.2e\n', abs(I2 - I_real2));

% Comparación con otros métodos
comparar_metodos_integracion(f2, 0, pi, I_real2);


function comparar_metodos_integracion(f, a, b, I_real)
% Compara Trapecio, Simpson y Romberg

    fprintf('\n\n');
    fprintf('═══════════════════════════════════════\n');
    fprintf('COMPARACIÓN DE MÉTODOS\n');
    fprintf('═══════════════════════════════════════\n\n');

    fprintf('%-20s %-10s %-20s %-15s %-15s\n', ...
            'Método', 'n/nivel', 'Resultado', 'Error', 'Evaluaciones');
    fprintf(repmat('─', 1, 80));
    fprintf('\n');

    % Trapecio
    [I_trap, ~] = trapecio_compuesto(f, a, b, 64);
    error_trap = abs(I_trap - I_real);
    fprintf('%-20s %-10d %-20.12f %-15.2e %-15d\n', ...
            'Trapecio', 64, I_trap, error_trap, 65);

    % Simpson
    [I_simp, ~] = simpson_1_3_compuesto(f, a, b, 64);
    error_simp = abs(I_simp - I_real);
    fprintf('%-20s %-10d %-20.12f %-15.2e %-15d\n', ...
            'Simpson 1/3', 64, I_simp, error_simp, 65);

    % Romberg
    [I_romb, ~] = romberg(f, a, b, 7, 1e-15, false);
    error_romb = abs(I_romb - I_real);
    evals_romb = 1 + 2 + 4 + 8 + 16 + 32 + 64;
    fprintf('%-20s %-10d %-20.12f %-15.2e %-15d\n', ...
            'Romberg', 6, I_romb, error_romb, evals_romb);

    fprintf('\n💡 Observación:\n');
    fprintf('   Romberg es %.0fx más preciso que Trapecio\n', error_trap/error_romb);
    fprintf('   Romberg es %.0fx más preciso que Simpson\n', error_simp/error_romb);

    % Graficar
    graficar_convergencia_romberg(f, a, b, I_real);
end


function graficar_convergencia_romberg(f, a, b, I_real)
% Grafica convergencia de Romberg

    [~, R] = romberg(f, a, b, 10, 0, false);

    n_niveles = size(R, 1);
    niveles = 0:(n_niveles-1);
    errores = zeros(1, n_niveles);

    for i = 1:n_niveles
        errores(i) = abs(R(i, i) - I_real);
    end

    % Filtrar valores válidos
    validos = errores > 0;
    niveles = niveles(validos);
    errores = errores(validos);

    figure('Position', [100, 100, 800, 600]);
    semilogy(niveles, errores, 'bo-', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'b');
    grid on;
    xlabel('Nivel de Romberg', 'FontSize', 12);
    ylabel('Error absoluto', 'FontSize', 12);
    title('Convergencia del Método de Romberg', 'FontSize', 14, 'FontWeight', 'bold');

    % Anotaciones
    for i = 1:min(5, length(niveles))
        text(niveles(i), errores(i)*1.5, sprintf('%.2e', errores(i)), ...
             'HorizontalAlignment', 'center', 'FontSize', 9);
    end

    fprintf('\n✅ Gráfica generada\n');
end