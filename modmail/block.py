

async def safe_block_user(user, config):
  """Safely handles blocking user"""
  async with config.blocked() as blocked:
    if user.id in blocked:
            return False
    blocked.append(user.id)
    return True

async def safe_unblock_user(user, config):
  """Safely handle unblocking the user"""
  async with config.blocked() as blocked:
    if user.id not in blocked:
      return False
    blocked.remove(user.id)
    return True