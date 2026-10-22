<?php

test('models adhere to strict typing and no debug statements')
    ->expect('App\Models')
    ->toUseStrictTypes()
    ->not->toUse(['dd', 'dump', 'var_dump']);
