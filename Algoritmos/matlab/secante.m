function [raiz, iteraciones] = secante(f, x0, x1, tol, max_iter)
% SECANTE Método de la Secante para encontrar raíces
%
% Sintaxis: [raiz, iteraciones] = secante(f, x0, x1, tol, max_iter)
%
% Parámetros:
%   f        - Handle de la función
%   x0, x1   - Dos aproximaciones iniciales
%   tol      - Tolerancia (opcional, default: 1e-6)
%   max_iter - Máximo de iteraciones (opcional, default: 100)
%
% Retorna:
%   raiz        - Aproximación de la raíz
%   iteraciones - Matriz con historial

    % Valores por defecto
    if nargin < 4, tol = 1e-6; end
    if nargin < 5, max_iter = 100; end

    % Inicialización
    x_ant = x0;
    x_act = x1;
    iteraciones = zeros(max_iter, 7);

    for i = 1:max_iter
        f_ant = f(x_ant);
        f_act = f(x_act);

        % Verificar división por cero
        if abs(f_act - f_ant) < 1e-10
            fprintf('Error: División por cero en iteración %d\n', i);
            raiz = NaN;
            iteraciones = iteraciones(1:i-1, :);
            return;
        end

        x_nuevo = x_act - f_act * (x_act - x_ant) / (f_act - f_ant);
        error = abs(x_nuevo - x_act);

        % Guardar iteración
        iteraciones(i, :) = [i, x_ant, x_act, f_ant, f_act, x_nuevo, error];

        % Criterio de convergencia
        if error < tol
            fprintf('Convergencia alcanzada en %d iteraciones\n', i);
            raiz = x_nuevo;
            iteraciones = iteraciones(1:i, :);
            return;
        end

        x_ant = x_act;
        x_act = x_nuevo;
    end

    fprintf('No se alcanzó convergencia en %d iteraciones\n', max_iter);
    raiz = x_act;
    iteraciones = iteraciones(1:max_iter, :);
end

% Ejemplo de uso:
% f = @(x) cos(x) - x;
% [raiz, hist] = secante(f, 0, 1);
% fprintf('Raíz encontrada: %.10f\n', raiz);