function [raiz, iteraciones] = biseccion(f, a, b, tol, max_iter)
% BISECCION Método de Bisección para encontrar raíces
%
% Sintaxis: [raiz, iteraciones] = biseccion(f, a, b, tol, max_iter)
%
% Parámetros:
%   f        - Handle de la función
%   a, b     - Extremos del intervalo [a, b]
%   tol      - Tolerancia (opcional, default: 1e-6)
%   max_iter - Máximo de iteraciones (opcional, default: 100)
%
% Retorna:
%   raiz        - Aproximación de la raíz
%   iteraciones - Matriz con historial

    % Valores por defecto
    if nargin < 4, tol = 1e-6; end
    if nargin < 5, max_iter = 100; end

    % Verificar condición inicial
    fa = f(a);
    fb = f(b);

    if fa * fb > 0
        error('f(a) y f(b) deben tener signos opuestos');
    end

    % Inicialización
    iteraciones = zeros(max_iter, 8);

    for i = 1:max_iter
        c = (a + b) / 2;
        fc = f(c);
        longitud = b - a;

        % Guardar iteración
        iteraciones(i, :) = [i, a, b, c, fa, fb, fc, longitud];

        % Criterio de convergencia
        if abs(fc) < tol || longitud/2 < tol
            fprintf('Convergencia alcanzada en %d iteraciones\n', i);
            raiz = c;
            iteraciones = iteraciones(1:i, :);
            return;
        end

        % Actualizar intervalo
        if fa * fc < 0
            b = c;
            fb = fc;
        else
            a = c;
            fa = fc;
        end
    end

    fprintf('No se alcanzó convergencia en %d iteraciones\n', max_iter);
    raiz = (a + b) / 2;
    iteraciones = iteraciones(1:max_iter, :);
end

% Ejemplo de uso:
% f = @(x) x^3 - x - 2;
% [raiz, hist] = biseccion(f, 1, 2);
% fprintf('Raíz encontrada: %.10f\n', raiz);