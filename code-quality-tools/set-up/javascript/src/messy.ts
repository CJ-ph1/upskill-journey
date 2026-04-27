import {foo,bar}   from "./does-not-exist"   // ❌ Prettier: spacing  ❌ ESLint: unused (after fix)

const   unused = 42                            // ❌ ESLint: unused variable

function add(a:number,b:number):number{return a-b}   // ❌ Prettier: spacing  ❌ logic bug

function greet(name) {                          // ❌ TypeScript (strict): implicit any
  if (name == null) return "hi"                 // ❌ ESLint: prefer === over ==
  console.log("debug",name)                     // ❌ ESLint (warn): no-console
  return "hi " + name
}

const result: number = add("1" as unknown as number, "2" as unknown as number)
// ↑ Even with the cast, this demonstrates how loose typing hides bugs.
// Remove the casts and TypeScript will report:
//   Argument of type 'string' is not assignable to parameter of type 'number'.

const out:string = result.toUpperCase()         // ❌ TypeScript: number has no toUpperCase
console.log(out)

export {greet, add}
