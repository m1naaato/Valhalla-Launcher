// Priority: 900
/**
 * @author vyrriox
 */
StartupEvents.registry('block', event => {
    event.create('arcadia:atm')
        .displayName('ATM')
        .soundType('metal')
        .hardness(5.0)
        .resistance(6.0)
        .requiresTool(true)
        .tagBlock('mineable/pickaxe')
        .tagBlock('needs_iron_tool')
        .texture('arcadia:block/atm')
})
