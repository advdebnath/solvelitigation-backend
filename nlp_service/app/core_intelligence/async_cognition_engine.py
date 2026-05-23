# =========================================================
# 🔥 ASYNCHRONOUS LEGAL COGNITION ENGINE
# =========================================================

import asyncio

# =========================================================
# 🔥 ASYNC WRAPPER
# =========================================================

async def execute_agent(

    agent_name,
    agent_callable,
    kwargs
):

    try:

        result = agent_callable(**kwargs)

        return {

            "agent":
                agent_name,

            "success":
                True,

            "result":
                result
        }

    except Exception as e:

        return {

            "agent":
                agent_name,

            "success":
                False,

            "error":
                str(e)
        }

# =========================================================
# 🔥 PARALLEL COGNITION EXECUTION
# =========================================================

async def execute_parallel_cognition(

    resolved_agents,
    shared_context
):

    tasks = []

    for agent_name, agent_callable in resolved_agents.items():

        task = execute_agent(

            agent_name,
            agent_callable,
            shared_context
        )

        tasks.append(task)

    results = await asyncio.gather(*tasks)

    cognition_results = {}

    for item in results:

        cognition_results[
            item["agent"]
        ] = item

    return cognition_results
