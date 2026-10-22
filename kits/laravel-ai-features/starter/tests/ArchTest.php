<?php

test('services adhere to strict typing and zero debugging calls')
    ->expect('App\Services')
    ->toUseStrictTypes()
    ->not->toUse(['dd', 'dump', 'var_dump']);
